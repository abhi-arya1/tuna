"""

Learning Docs for Tuna Learn Commands and Quickstart Notebooks

"""

from tuna.cli.core.constants import BLUE, RESET, ITALIC, BOLD, CDOT

# pylint: disable=line-too-long


NOTEBOOK_CONSTANTS = {
    "mistral": "https://github.com/abhi-arya1/tuna/blob/main/notebooks/quickstarts/mistral.ipynb",
    "llama"  : "https://github.com/abhi-arya1/tuna/blob/main/notebooks/quickstarts/llama.ipynb",
    "gemma"  : "https://github.com/abhi-arya1/tuna/blob/main/notebooks/quickstarts/gemma.ipynb",
}




LEARNER = {
    "base_model": 
f"""
{BLUE}Base Model{RESET}: The initial pre-trained model that provides a starting point for further fine-tuning or transfer learning.
{ITALIC}{CDOT} You can pick a base model for Tuna at {BOLD}https://huggingface.co/models?pipeline_tag=text-generation"{RESET}
""",
    "fine_tuning": f"""{BLUE}Fine-Tuning{RESET}: The process of taking a pre-trained model and training it further on a specific dataset to specialize it for a particular task.
    """,
    "transfer_learning": f"""{BLUE}Transfer Learning{RESET}: A machine learning technique where a model developed for a particular task is reused as the starting point for a model on a second task.
    """,
    "learning_rate": f"""{BLUE}Learning Rate{RESET}: A hyperparameter that controls how much to change the model in response to the estimated error each time the model weights are updated.
    """,
    "batch_size": f"""{BLUE}Batch Size{RESET}: The number of training examples utilized in one iteration of model training.
    """,
    "epoch": f"""{BLUE}Epoch{RESET}: One complete pass through the entire training dataset.
    """,
    "overfitting": f"""{BLUE}Overfitting{RESET}: A modeling error that occurs when a function is too closely fit to a limited set of data points, capturing noise rather than the underlying distribution.
    """,
    "underfitting": f"""{BLUE}Underfitting{RESET}: A modeling error that occurs when a model is too simple to capture the underlying pattern of the data.
    """,
    "gradient_descent": f"""{BLUE}Gradient Descent{RESET}: An optimization algorithm used to minimize the loss function by iteratively moving towards the steepest descent direction.
    """,
    "backpropagation": f"""{BLUE}Backpropagation{RESET}: A training algorithm for neural networks where gradients are calculated and propagated backward through the network to update the weights.
    """,
    "neural_network": f"""{BLUE}Neural Network{RESET}: A computational model inspired by the way biological neural networks in the human brain process information.
    """,
    "activation_function": f"""{BLUE}Activation Function{RESET}: A function applied to a neuron’s output in a neural network to introduce non-linearities into the model.
    """,
    "dropout": f"""{BLUE}Dropout{RESET}: A regularization technique where randomly selected neurons are ignored during training to prevent overfitting.
    """,
    "regularization": f"""{BLUE}Regularization{RESET}: Techniques used to prevent overfitting by adding additional constraints or penalties to the model.
    """,
    "loss_function": f"""{BLUE}Loss Function{RESET}: A function that measures the difference between the predicted output and the actual output during training.
    """,
    "hyperparameter": f"""{BLUE}Hyperparameter{RESET}: A parameter whose value is set before the learning process begins and controls the behavior of the training algorithm.
    """,
    "model_evaluation": f"""{BLUE}Model Evaluation{RESET}: The process of assessing the performance of a trained model using various metrics and validation techniques.
    """,
    "cross_validation": f"""{BLUE}Cross-Validation{RESET}: A technique for assessing how the results of a statistical analysis will generalize to an independent dataset.
    """,
    "precision": f"""{BLUE}Precision{RESET}: A metric that measures the number of true positive results divided by the number of all positive results, including those not identified correctly.
    """,
    "recall": f"""{BLUE}Recall{RESET}: A metric that measures the number of true positive results divided by the number of positives that should have been identified.
    """,
    "f1_score": f"""{BLUE}F1 Score{RESET}: A metric that combines precision and recall into a single score by calculating their harmonic mean.
    """,
    "words": f"""
{BOLD}{BLUE}[word] options for `tuna learn [word]`{RESET}
{ITALIC}{CDOT} base_model{RESET}
{ITALIC}{CDOT} fine_tuning{RESET}
{ITALIC}{CDOT} transfer_learning{RESET}
{ITALIC}{CDOT} learning_rate{RESET}
{ITALIC}{CDOT} batch_size{RESET}
{ITALIC}{CDOT} epoch{RESET}
{ITALIC}{CDOT} overfitting{RESET}
{ITALIC}{CDOT} underfitting{RESET}
{ITALIC}{CDOT} gradient_descent{RESET}
{ITALIC}{CDOT} backpropagation{RESET}
{ITALIC}{CDOT} neural_network{RESET}
{ITALIC}{CDOT} activation_function{RESET}
{ITALIC}{CDOT} dropout{RESET}
{ITALIC}{CDOT} regularization{RESET}
{ITALIC}{CDOT} loss_function{RESET}
{ITALIC}{CDOT} hyperparameter{RESET}
{ITALIC}{CDOT} model_evaluation{RESET}
{ITALIC}{CDOT} cross_validation{RESET}
{ITALIC}{CDOT} precision{RESET}
{ITALIC}{CDOT} recall{RESET}
{ITALIC}{CDOT} f1_score{RESET}
"""
}
