import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

class MLModelManager:
    _instance = None

    def __new__(cls):
            if cls._instance is None:
                cls._instance = super(MLModelManager, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        model_path = "./ml_models"

        print("Loding ML Model")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.eval()

        self.pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        print("ML Model loaded successfully")

    def predict_category(self, text):
        """Predicts the category"""
        with torch.no_grad():
            result = self.pipeline(text, truncation=True, max_length=128)[0]
        return result['label']

ml_model_instance = MLModelManager()
    

