import yake
import PyPDF2
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resource

@receiver(post_save, sender=Resource)
def extract_keywords_from_resource(sender, instance, created, **kwargs):
    """
    Extracts keywords from a resource file (PDF) after it's saved
    and updates the keywords field.
    """
    if created:  # Only run when a new resource is created
        try:
            # --- Text Extraction from PDF ---
            file_content = instance.file.read()
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""

            if not text.strip():
                # No text could be extracted
                instance.keywords = []
                instance.save(update_fields=['keywords'])
                return

            # --- Keyword Extraction using YAKE ---
            language = "fr"  # Assuming French for now
            max_ngram_size = 3
            deduplication_threshold = 0.9
            num_of_keywords = 20
            
            custom_kw_extractor = yake.KeywordExtractor(
                lang=language, 
                n=max_ngram_size, 
                dedupLim=deduplication_threshold, 
                top=num_of_keywords, 
                features=None
            )
            
            keywords_tuples = custom_kw_extractor.extract_keywords(text)
            keywords = [kw for kw, score in keywords_tuples]

            # --- Update the resource instance ---
            instance.keywords = keywords
            instance.save(update_fields=['keywords'])

        except Exception as e:
            # Handle cases where the file might not be a valid PDF or other errors
            print(f"Error extracting keywords for resource {instance.id}: {e}")
            instance.keywords = []
            instance.save(update_fields=['keywords']) 