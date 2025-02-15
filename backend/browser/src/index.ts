import { Hono } from 'hono'
import { Stagehand } from '@browserbasehq/stagehand'
import { z } from 'zod'
import { config } from 'dotenv';
import { createBunWebSocket } from "hono/bun";
import type { ServerWebSocket } from "bun";

const { upgradeWebSocket, websocket } = createBunWebSocket<ServerWebSocket>();

config({
  path: "../.env"
});

const app = new Hono()

app.get('/', (c) => {
  return c.text(`Hello from Tuna-Stagehand`);
});

app.get(
  "/ws",
  upgradeWebSocket((c) => {
    return {
      async onMessage(event, ws) {
        const data = JSON.parse(event.data.toString());
        console.log(data);

        const url = data.url;
        const instruction = data.instruction; 

        let retries = 0;
        let maxRetries = 3;
        let content = null;

        const stagehand = new Stagehand({
          env: "LOCAL",
          verbose: 1,
          debugDom: true,
          domSettleTimeoutMs: 100,
          logger: (msg) => {
            console.log(msg);
            ws.send(JSON.stringify({ complete: false, log: msg }));
          },
          modelName: "claude-3-5-sonnet-latest",
          modelClientOptions: {
            apiKey: "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"
          }
        });

        while (retries < maxRetries) {
          try {

            await stagehand.init();
            await stagehand.page.goto(url);

            content = await stagehand.page.extract({
              instruction: `${instruction}. PROVIDE EXACTLY 3 EXAMPLES THAT VARY A BIT AND STOP EXTRACTING DATA AS SOON AS YOU REACH 3. YOU MUST USE YOUR TOOLS IN EVERY RESPONSE.`,
              schema: z.object({
                examples: z.array(z.object({
                  requested_item: z.string(),
                  item_detail: z.string()
                }))
              }),
            });

            // If successful, send data and break loop
            ws.send(JSON.stringify({ 
              complete: true,
              data: content,
              log: "Completed data extraction"
            }));
            break;

          } catch (error) {
            retries++;
            console.error(`Error occurred (attempt ${retries} of ${maxRetries}):`, error);

            // If retries exceed limit, send final error and close connection
            if (retries === maxRetries) {
              ws.send(JSON.stringify({ complete: true, error: "Maximum retries reached. Extraction failed." }));
              ws.close();
            }
          }
        }
      },
      onClose: () => {
        console.log("Connection closed");
      },
    };
  })
);

// Start Hono server with Bun
export default {
  fetch: app.fetch,
  websocket,
  port: 8080,
};
