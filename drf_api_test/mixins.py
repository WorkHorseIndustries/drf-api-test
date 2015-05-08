
class OptionsAllowedMethodsMixin(object):

    def metadata(self, request):
        try: 
            data = super(OptionsAllowedMethodsMixin, self).metadata(request)
        except:
            data = {}

        methods = [('get', 'GET'), 
                ('post', 'POST'), 
                ('put', 'PUT'),
                ('patch', 'PATCH'),
                ('delete', 'DELETE')]

        data.setdefault('allowed_methods', [])
        for m in methods:
            if hasattr(self, m[0]):
                data['allowed_methods'].append(m[1])
        return data
