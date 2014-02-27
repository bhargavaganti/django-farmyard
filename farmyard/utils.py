import urllib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def google_lat_long(location):
    try:
        key=settings.GOOGLE_API_KEY
    except:
        logger.debug('No Google API key set.')
        key=''

    output = "csv"
    location = urllib.quote_plus(location)
    logging.debug('onec_utils.utils: google_lat_long() says "Requesting lat/long from Google."')
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        coords = "%s, %s" % (dlist[2], dlist[3])
    else:
        coords = ''
    return coords

def get_fancy_time(rdelta, display_full_version = False):
    """Returns a user friendly date format
    d: some datetime instace in the past
    display_second_unit: True/False
    """
    #some helpers lambda's
    plural = lambda x: 's' if x > 1 else ''
    singular = lambda x: x[:-1]
    #convert pluran (years) --> to singular (year)
    display_unit = lambda unit, name: '%s %s%s'%(unit, name, plural(unit)) if unit > 0 else ''

    #time units we are interested in descending order of significance
    tm_units = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

    for idx, tm_unit in enumerate(tm_units):
        first_unit_val = getattr(rdelta, tm_unit)
        if first_unit_val > 0:
            primary_unit = display_unit(first_unit_val, singular(tm_unit))
            if display_full_version and idx < len(tm_units)-1:
                next_unit = tm_units[idx + 1]
                second_unit_val = getattr(rdelta, next_unit)
                if second_unit_val > 0:
                    secondary_unit = display_unit(second_unit_val, singular(next_unit))
                    return primary_unit + ', ' + secondary_unit
            return primary_unit
    return None

if __name__ == "__main__":
    data_sets = [datetime.utcnow() + relativedelta(seconds=-3),
                        datetime.utcnow() + relativedelta(minutes=-2, seconds=-6),
                        datetime.utcnow() + relativedelta(minutes=-65, seconds=-50),
                        datetime.utcnow() + relativedelta(days=-2, minutes=-2),
                        datetime.utcnow() + relativedelta(months=-2, days=-45),
                        datetime.utcnow() + relativedelta(months=-54)]

    for x in data_sets:
        print '%s' % (get_fancy_time(x, display_full_version = True))


ANIMAL_FEMALE_NAMES={
        'pig':     'sow',
        'chicken': 'hen',
        'goat':    'doe',
        'dog':     'bitch',
        'sheep':   'ewe'}

def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value
