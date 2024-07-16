# pylint: disable=all

# import os
# import json
# import matplotlib.pyplot as plt
# from datetime import datetime
# from transformers import TrainerCallback
# from tuna.cli.core.constants import TUNA_DIR



# class CustomCallback(TrainerCallback):
#     def __init__(self, tracker):
#         self.tracker = tracker

#     def on_log(self, args, state, control, logs=None, **kwargs):
#         if logs is not None:
#             for key, value in logs.items():
#                 self.tracker.log_metric(key, value, state.global_step)



# class LocalTracker:
#     def __init__(self, experiment_name):
#         self.experiment_name = experiment_name
#         self.save_dir = TUNA_DIR
#         self.data = {
#             'experiment_name': self.experiment_name,
#             'metrics': [],
#             'hyperparameters': {},
#             'model_paths': []
#         }
#         self.experiment_path = os.path.join(self.save_dir, self.experiment_name)
#         os.makedirs(self.experiment_path, exist_ok=True)

#     def log_metric(self, name, value, step):
#         """
#         Logs a metric value at a given step.
#         """
#         self.data['metrics'].append({'name': name, 'value': value, 'step': step, 'timestamp': str(datetime.now())})
#         self._save_data()

#     def log_hyperparameter(self, name, value):
#         self.data['hyperparameters'][name] = value
#         self._save_data()

#     def save_model(self, model_path):
#         self.data['model_paths'].append(model_path)
#         self._save_data()

#     def _save_data(self):
#         with open(os.path.join(self.experiment_path, 'experiment_data.json'), 'w') as f:
#             json.dump(self.data, f, indent=4)

#     def plot_metrics(self):
#         metrics = self.data['metrics']
#         if not metrics:
#             print("No metrics to plot.")
#             return

#         metrics_by_name = {}
#         for metric in metrics:
#             name = metric['name']
#             if name not in metrics_by_name:
#                 metrics_by_name[name] = {'steps': [], 'values': []}
#             metrics_by_name[name]['steps'].append(metric['step'])
#             metrics_by_name[name]['values'].append(metric['value'])

#         for name, data in metrics_by_name.items():
#             plt.figure()
#             plt.plot(data['steps'], data['values'], label=name)
#             plt.xlabel('Step')
#             plt.ylabel(name)
#             plt.title(f'{name} over Steps')
#             plt.legend()
#             plt.grid(True)
#             plt_path = os.path.join(self.experiment_path, f'{name}_plot.png')
#             plt.savefig(plt_path)
#             plt.close()
#             print(f"Saved plot: {plt_path}")
