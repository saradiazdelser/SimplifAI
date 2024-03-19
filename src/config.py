import logging
import os


class Configuration:
    """
    Configuration for inference with Local Server
    """

    HOST: str = os.getenv("HOST", "10.10.78.11")
    PORT: int = int(os.getenv("PORT", "8081"))

    MAX_NEW_TOKENS: int = 512
    TOP_K: int = 10
    TOP_P: float = 0.95
    TYPICAL_P: float = 0.95
    TEMPERATURE: float = 0.01

    def __init__(self):
        self.LLM_CONFIG = self.__load_llm_config()
        self.__import_libraries()  # import spacy model if necessary

    def __import_libraries(self):
        import spacy

        # Check if the model exists
        if not spacy.util.is_package("en_core_web_sm"):
            logging.info("Couldn't find spacy model en_core_web_sm. Downloading.")
            # If not, download it
            spacy.cli.download("en_core_web_sm")

    def __load_llm_config(self):
        return {
            "inference_server_url": f"http://{self.HOST}:{str(self.PORT)}/",
            "max_new_tokens": self.MAX_NEW_TOKENS,
            "top_k": self.TOP_K,
            "top_p": self.TOP_P,
            "typical_p": self.TYPICAL_P,
            "temperature": self.TEMPERATURE,
        }
