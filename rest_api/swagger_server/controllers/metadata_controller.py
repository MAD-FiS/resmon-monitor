import connexion
import six

from rest_api.swagger_server.models.metadata_tag import MetadataTag  # noqa: E501
from rest_api.swagger_server import util


def get_metadata():  # noqa: E501
    """List of all available hosts metadata

     # noqa: E501


    :rtype: List[MetadataTag]
    """
    return 'do some magic!'
