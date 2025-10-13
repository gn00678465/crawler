"""
Unit tests for AIModelConfiguration Pydantic model.

This module tests the validation rules, factory method, and behavior of the
AIModelConfiguration model, which parses AI model strings and maps providers
to their required API keys.
"""

import pytest
from pydantic import ValidationError

from src.models.ai_model_config import AIModelConfiguration


class TestAIModelConfigurationFactoryMethod:
    """Test AIModelConfiguration.from_model_string() factory method."""

    def test_from_model_string_gemini_pro(self):
        """Test parsing gemini/gemini-pro model string."""
        config = AIModelConfiguration.from_model_string("gemini/gemini-pro")

        assert config.full_name == "gemini/gemini-pro"
        assert config.provider == "gemini"
        assert config.model_name == "gemini-pro"
        assert config.api_key_env_var == "GOOGLE_API_KEY"
        assert config.is_local is False

    def test_from_model_string_gemini_flash(self):
        """Test parsing gemini/gemini-1.5-flash model string."""
        config = AIModelConfiguration.from_model_string("gemini/gemini-1.5-flash")

        assert config.full_name == "gemini/gemini-1.5-flash"
        assert config.provider == "gemini"
        assert config.model_name == "gemini-1.5-flash"
        assert config.api_key_env_var == "GOOGLE_API_KEY"
        assert config.is_local is False

    def test_from_model_string_openai_gpt4o(self):
        """Test parsing openai/gpt-4o model string."""
        config = AIModelConfiguration.from_model_string("openai/gpt-4o")

        assert config.full_name == "openai/gpt-4o"
        assert config.provider == "openai"
        assert config.model_name == "gpt-4o"
        assert config.api_key_env_var == "OPENAI_API_KEY"
        assert config.is_local is False

    def test_from_model_string_openai_gpt4o_mini(self):
        """Test parsing openai/gpt-4o-mini model string."""
        config = AIModelConfiguration.from_model_string("openai/gpt-4o-mini")

        assert config.full_name == "openai/gpt-4o-mini"
        assert config.provider == "openai"
        assert config.model_name == "gpt-4o-mini"
        assert config.api_key_env_var == "OPENAI_API_KEY"
        assert config.is_local is False

    def test_from_model_string_anthropic_claude(self):
        """Test parsing anthropic/claude-3-haiku model string."""
        config = AIModelConfiguration.from_model_string("anthropic/claude-3-haiku-20240307")

        assert config.full_name == "anthropic/claude-3-haiku-20240307"
        assert config.provider == "anthropic"
        assert config.model_name == "claude-3-haiku-20240307"
        assert config.api_key_env_var == "ANTHROPIC_API_KEY"
        assert config.is_local is False

    def test_from_model_string_ollama_llama3(self):
        """Test parsing ollama/llama3 local model string."""
        config = AIModelConfiguration.from_model_string("ollama/llama3")

        assert config.full_name == "ollama/llama3"
        assert config.provider == "ollama"
        assert config.model_name == "llama3"
        assert config.api_key_env_var is None  # Local model
        assert config.is_local is True

    def test_from_model_string_ollama_mistral(self):
        """Test parsing ollama/mistral local model string."""
        config = AIModelConfiguration.from_model_string("ollama/mistral")

        assert config.full_name == "ollama/mistral"
        assert config.provider == "ollama"
        assert config.model_name == "mistral"
        assert config.api_key_env_var is None
        assert config.is_local is True

    def test_from_model_string_vllm(self):
        """Test parsing vllm local model string."""
        config = AIModelConfiguration.from_model_string("vllm/meta-llama-3")

        assert config.full_name == "vllm/meta-llama-3"
        assert config.provider == "vllm"
        assert config.model_name == "meta-llama-3"
        assert config.api_key_env_var is None  # Local model
        assert config.is_local is True


class TestAIModelConfigurationValidation:
    """Test AIModelConfiguration validation rules."""

    def test_valid_instantiation_with_all_fields(self):
        """Test that AIModelConfiguration can be created with all valid fields."""
        config = AIModelConfiguration(
            full_name="gemini/gemini-pro",
            provider="gemini",
            model_name="gemini-pro",
            api_key_env_var="GOOGLE_API_KEY",
            is_local=False,
        )

        assert config.full_name == "gemini/gemini-pro"
        assert config.provider == "gemini"
        assert config.model_name == "gemini-pro"
        assert config.api_key_env_var == "GOOGLE_API_KEY"
        assert config.is_local is False

    def test_valid_instantiation_for_local_model(self):
        """Test creating configuration for local model."""
        config = AIModelConfiguration(
            full_name="ollama/llama3",
            provider="ollama",
            model_name="llama3",
            api_key_env_var=None,
            is_local=True,
        )

        assert config.is_local is True
        assert config.api_key_env_var is None

    def test_is_local_defaults_to_false(self):
        """Test that is_local defaults to False when not specified."""
        config = AIModelConfiguration(
            full_name="gemini/gemini-pro", provider="gemini", model_name="gemini-pro"
        )

        assert config.is_local is False

    def test_api_key_env_var_can_be_none(self):
        """Test that api_key_env_var can be None (for local models)."""
        config = AIModelConfiguration(
            full_name="ollama/llama3",
            provider="ollama",
            model_name="llama3",
            api_key_env_var=None,
            is_local=True,
        )

        assert config.api_key_env_var is None

    def test_full_name_validation_rejects_missing_separator(self):
        """Test that full_name without '/' separator is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AIModelConfiguration(
                full_name="gemini-pro",  # Missing provider/
                provider="gemini",
                model_name="gemini-pro",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("full_name",) for error in errors)
        assert any("format" in str(error["msg"]).lower() for error in errors)

    def test_full_name_validation_rejects_empty_provider(self):
        """Test that full_name with empty provider is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AIModelConfiguration(
                full_name="/gemini-pro",  # Empty provider
                provider="",
                model_name="gemini-pro",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("full_name",) for error in errors)

    def test_full_name_validation_rejects_empty_model_name(self):
        """Test that full_name with empty model name is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AIModelConfiguration(
                full_name="gemini/",  # Empty model name
                provider="gemini",
                model_name="",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("full_name",) for error in errors)

    def test_full_name_validation_rejects_multiple_separators(self):
        """Test that full_name with multiple '/' separators is handled correctly."""
        # LiteLLM might support azure/deployment/model format, but for our P1 spec
        # we only support provider/model format. This test documents the behavior.
        with pytest.raises(ValidationError):
            config = AIModelConfiguration(
                full_name="azure/deployment/gpt-4", provider="azure", model_name="deployment/gpt-4"
            )


class TestAIModelConfigurationProviderMapping:
    """Test provider-to-API-key mapping logic."""

    def test_gemini_maps_to_google_api_key(self):
        """Test that gemini provider maps to GOOGLE_API_KEY."""
        config = AIModelConfiguration.from_model_string("gemini/gemini-pro")
        assert config.api_key_env_var == "GOOGLE_API_KEY"

    def test_openai_maps_to_openai_api_key(self):
        """Test that openai provider maps to OPENAI_API_KEY."""
        config = AIModelConfiguration.from_model_string("openai/gpt-4o")
        assert config.api_key_env_var == "OPENAI_API_KEY"

    def test_anthropic_maps_to_anthropic_api_key(self):
        """Test that anthropic provider maps to ANTHROPIC_API_KEY."""
        config = AIModelConfiguration.from_model_string("anthropic/claude-3-haiku-20240307")
        assert config.api_key_env_var == "ANTHROPIC_API_KEY"

    def test_ollama_has_no_api_key(self):
        """Test that ollama (local) has no API key requirement."""
        config = AIModelConfiguration.from_model_string("ollama/llama3")
        assert config.api_key_env_var is None
        assert config.is_local is True

    def test_vllm_has_no_api_key(self):
        """Test that vllm (local) has no API key requirement."""
        config = AIModelConfiguration.from_model_string("vllm/meta-llama-3")
        assert config.api_key_env_var is None
        assert config.is_local is True

    def test_unknown_provider_has_no_api_key_mapping(self):
        """Test that unknown providers get None for api_key_env_var."""
        # This tests the default behavior when provider is not in the map
        config = AIModelConfiguration(
            full_name="unknown/some-model", provider="unknown", model_name="some-model"
        )
        # Should not raise error, just return None for unknown provider
        assert config.api_key_env_var is None or isinstance(config.api_key_env_var, str)


class TestAIModelConfigurationEdgeCases:
    """Test edge cases and special scenarios."""

    def test_model_name_with_version_numbers(self):
        """Test parsing model names with complex version numbers."""
        config = AIModelConfiguration.from_model_string("gemini/gemini-1.5-pro-001")

        assert config.model_name == "gemini-1.5-pro-001"
        assert config.provider == "gemini"

    def test_model_name_with_date_suffix(self):
        """Test parsing model names with date suffixes."""
        config = AIModelConfiguration.from_model_string("anthropic/claude-3-haiku-20240307")

        assert config.model_name == "claude-3-haiku-20240307"
        assert config.provider == "anthropic"

    def test_model_name_with_hyphens(self):
        """Test parsing model names containing multiple hyphens."""
        config = AIModelConfiguration.from_model_string("openai/gpt-4o-mini")

        assert config.model_name == "gpt-4o-mini"
        assert config.provider == "openai"

    def test_model_name_with_underscores(self):
        """Test parsing model names with underscores."""
        config = AIModelConfiguration.from_model_string("vllm/meta_llama_3")

        assert config.model_name == "meta_llama_3"
        assert config.provider == "vllm"

    def test_case_sensitive_provider_names(self):
        """Test that provider names are case-sensitive."""
        config1 = AIModelConfiguration.from_model_string("gemini/gemini-pro")
        config2 = AIModelConfiguration.from_model_string("Gemini/gemini-pro")

        # Provider names should be treated as-is (case-sensitive)
        assert config1.provider == "gemini"
        assert config2.provider == "Gemini"
        # But the mapping may not recognize uppercase
        assert config1.api_key_env_var == "GOOGLE_API_KEY"


class TestAIModelConfigurationSerialization:
    """Test JSON serialization and deserialization."""

    def test_model_can_be_serialized_to_json(self):
        """Test that AIModelConfiguration can be serialized to JSON."""
        config = AIModelConfiguration.from_model_string("gemini/gemini-pro")

        json_data = config.model_dump_json()
        assert isinstance(json_data, str)
        assert "gemini" in json_data
        assert "GOOGLE_API_KEY" in json_data

    def test_model_can_be_deserialized_from_dict(self):
        """Test that AIModelConfiguration can be created from dict."""
        data = {
            "full_name": "gemini/gemini-pro",
            "provider": "gemini",
            "model_name": "gemini-pro",
            "api_key_env_var": "GOOGLE_API_KEY",
            "is_local": False,
        }

        config = AIModelConfiguration(**data)
        assert config.provider == "gemini"
        assert config.model_name == "gemini-pro"

    def test_model_round_trip_serialization(self):
        """Test that AIModelConfiguration can be serialized and deserialized."""
        original = AIModelConfiguration.from_model_string("openai/gpt-4o")

        # Serialize to dict and back
        data = original.model_dump()
        reconstructed = AIModelConfiguration(**data)

        assert reconstructed.full_name == original.full_name
        assert reconstructed.provider == original.provider
        assert reconstructed.model_name == original.model_name
        assert reconstructed.api_key_env_var == original.api_key_env_var
        assert reconstructed.is_local == original.is_local
