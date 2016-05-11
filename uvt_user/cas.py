from django.contrib.auth import get_user_model
from .models import UvtUser
from .utils import search_ldap, LDAPError

def callback(tree):
    '''This function is called after every successful CAS authentication. It creates/updates the uvt_user attribute. Because this only happens here, users without a uvt_user attribute are guaranteed to be regular users.'''

    username = tree[0][0].text

    # The following line has the nasty side-effect of hijacking
    # existing user accounts whenever the CAS server returns a
    # username that is already in the database. For details, see this
    # StackOverflow question: http://stackoverflow.com/questions/37159321/
    # As a workaround, make sure not to create usernames in the admin
    # that might be valid UvT usernames.
    user, created = get_user_model().objects.get_or_create(username=username)
    uvt_user, created = UvtUser.objects.get_or_create(user=user)

    # Permission has been granted by TiU's legal department for
    # retrieving the following data:
    try:
        (
            uvt_user.first_name,
            uvt_user.full_name,
            uvt_user.ANR,
            uvt_user.email
        ) = search_ldap(username)
        uvt_user.save()

    except LDAPError:
        pass
