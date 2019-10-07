import os
import pytest
import ucp


def test_get_config():
    ucp.reset()
    config = ucp.get_config()
    assert isinstance(config, dict)
    assert config["MEMTYPE_CACHE"] == "n"


def test_set_env():
    ucp.reset()
    os.environ["UCX_SEG_SIZE"] = "2M"
    config = ucp.get_config()
    assert config["SEG_SIZE"] == os.environ["UCX_SEG_SIZE"]


def test_init_options():
    ucp.reset()
    os.environ["UCX_SEG_SIZE"] = "2M"  # Should be ignored
    options = {"SEG_SIZE": "3M"}
    ucp.init(options)
    config = ucp.get_config()
    assert config["SEG_SIZE"] == options["SEG_SIZE"]


def test_init_options_and_env():
    ucp.reset()
    os.environ["UCX_SEG_SIZE"] = "4M"
    options = {"SEG_SIZE": "3M"}  # Should be ignored
    ucp.init(options, env_takes_preceding=True)
    config = ucp.get_config()
    assert config["SEG_SIZE"] == options["SEG_SIZE"]


def test_init_unknown_option():
    ucp.reset()
    options = {"UNKNOWN_OPTION": "3M"}
    with pytest.raises(ucp.exceptions.UCXConfigError):
        ucp.init(options)


def test_init_invalid_option():
    ucp.reset()
    options = {"SEG_SIZE": "invalid-size"}
    with pytest.raises(ucp.exceptions.UCXConfigError):
        ucp.init(options)
