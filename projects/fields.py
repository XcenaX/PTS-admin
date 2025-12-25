from rest_framework import serializers

class ModelTranslationDictField(serializers.Field):
    """
    Представляет modeltranslation-поля как:
      {"ru": "...", "kz": "...", "en": "..."}
    И принимает такой же формат на запись.
    """
    api_to_mt = {"ru": "ru", "kz": "kk", "en": "en"}  # маппинг ключей API -> суффиксы modeltranslation

    def __init__(self, base_name: str, **kwargs):
        self.base_name = base_name
        super().__init__(**kwargs)

    def get_attribute(self, instance):
        # чтобы в to_representation иметь доступ к инстансу целиком
        return instance

    def to_representation(self, instance):
        out = {}
        for api_lang, mt_lang in self.api_to_mt.items():
            attr = f"{self.base_name}_{mt_lang}"
            out[api_lang] = getattr(instance, attr, None)
        return out

    def to_internal_value(self, data):
        if data is None:
            return {}

        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected object: {'ru': '...', 'kz': '...', 'en': '...'}")

        result = {}
        for api_lang, value in data.items():
            if api_lang not in self.api_to_mt:
                raise serializers.ValidationError(f"Unsupported language key: {api_lang}")

            mt_lang = self.api_to_mt[api_lang]
            result[f"{self.base_name}_{mt_lang}"] = value

        return result
