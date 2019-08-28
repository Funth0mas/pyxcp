
from unittest import mock

import pytest

import pyxcp.transport.base as tr
from test_master import MockCanInterface

def test_factory_works():
    assert isinstance(tr.createTransport("eth"), tr.BaseTransport)
    assert isinstance(tr.createTransport("sxi", port = 5555), tr.BaseTransport)
    assert isinstance(tr.createTransport("can", canInterface = MockCanInterface,
            config = {'CAN_ID_MASTER': 1, 'CAN_ID_SLAVE': 2}), tr.BaseTransport
                      )

def test_factory_works_case_insensitive():
    assert isinstance(tr.createTransport("ETH"), tr.BaseTransport)
    assert isinstance(tr.createTransport("SXI", port = 5555), tr.BaseTransport)
    assert isinstance(tr.createTransport("CAN", canInterface = MockCanInterface,
        config = {'CAN_ID_MASTER': 1, 'CAN_ID_SLAVE': 2}), tr.BaseTransport)

def test_factory_invalid_transport_name_raises():
    with pytest.raises(ValueError):
        tr.createTransport("xCp")

def test_transport_names():
    transports = tr.availableTransports()

    assert "can" in transports
    assert "eth" in transports
    assert "sxi" in transports

def test_transport_names_are_lower_case_only():
    transports = tr.availableTransports()

    assert "CAN" not in transports
    assert "ETH" not in transports
    assert "SXI" not in transports

def test_transport_classes():
    transports = tr.availableTransports()

    assert issubclass(transports.get("can"), tr.BaseTransport)
    assert issubclass(transports.get("eth"), tr.BaseTransport)
    assert issubclass(transports.get("sxi"), tr.BaseTransport)

