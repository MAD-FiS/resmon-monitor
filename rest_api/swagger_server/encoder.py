from connexion.apps.flask_app import FlaskJSONEncoder
import six

from rest_api.swagger_server.models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    """ Class for encode JSON"""
    include_nulls = False

    def default(self, o):
        """Method to encode JSON"""
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return FlaskJSONEncoder.default(self, o)
