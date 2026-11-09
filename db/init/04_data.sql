-- PostgreSQL initialisation for the portfolio database: reference data.

-- Link kinds used by social_links and experience_links. The patterns mostly check the
-- domain: a pattern too strict would reject valid URLs (a YouTube playlist, a LinkedIn
-- company page). The icons must exist in an installed Iconify collection.
INSERT INTO link_kinds (kind, url_pattern, icon) VALUES
    ('website',     '^https://[^/\s]+\.[^/\s]+',                                               'i-lucide-globe'),
    ('certificate', '^https://[^/\s]+\.[^/\s]+',                                               'i-lucide-award'),
    ('github',      '^https://github\.com/[A-Za-z0-9-]+(/[A-Za-z0-9._-]+)?/?$',                'i-simple-icons-github'),
    ('gitlab',      '^https://gitlab\.com/[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*/?$',              'i-simple-icons-gitlab'),
    ('linkedin',    '^https://([a-z]{2,3}\.)?linkedin\.com/(in|company|school)/[^/?#]+/?$',    'i-lucide-linkedin'),
    ('youtube',     '^https://(www\.|m\.)?(youtube\.com|youtu\.be)/',                          'i-simple-icons-youtube'),
    ('discord',     '^https://(discord\.gg|discord\.com/(invite|users))/[A-Za-z0-9]+/?$',      'i-simple-icons-discord'),
    ('instagram',   '^https://(www\.)?instagram\.com/[A-Za-z0-9._]+/?$',                       'i-simple-icons-instagram'),
    ('x',           '^https://(www\.)?(x|twitter)\.com/[A-Za-z0-9_]+/?$',                      'i-simple-icons-x'),
    ('artstation',  '^https://([A-Za-z0-9-]+\.)?artstation\.com(/|$)',                         'i-simple-icons-artstation'),
    ('behance',     '^https://(www\.)?behance\.net/[A-Za-z0-9_-]+',                            'i-simple-icons-behance'),
    ('tryhackme',   '^https://tryhackme\.com/',                                                'i-simple-icons-tryhackme'),
    ('flickr',      '^https://(www\.)?(flickr\.com|flic\.kr)/',                                'i-simple-icons-flickr'),
    ('kofi',        '^https://(www\.)?ko-fi\.com/[A-Za-z0-9_]+/?$',                            'i-simple-icons-kofi'),
    ('patreon',     '^https://(www\.)?patreon\.com/[^/?#]+',                                   'i-simple-icons-patreon'),
    -- No Tipeee icon in simple-icons.
    ('tipeee',      '^https://([a-z]{2}\.)?tipeee\.com/[^/?#]+',                               'i-lucide-hand-coins'),
    ('paypal',      '^https://(www\.)?(paypal\.me|paypal\.com)/',                              'i-simple-icons-paypal'),
    ('trustpilot',  '^https://([a-z]{2}\.|www\.)?trustpilot\.com/review/',                     'i-simple-icons-trustpilot'),
    ('distrokid',   '^https://(www\.)?distrokid\.com/',                                        'i-simple-icons-distrokid'),
    ('spotify',     '^https://open\.spotify\.com/',                                            'i-simple-icons-spotify'),
    ('apple_music', '^https://music\.apple\.com/',                                             'i-simple-icons-applemusic'),
    ('deezer',      '^https://(([a-z]+\.)?deezer\.com|deezer\.page\.link)/',                   'i-simple-icons-deezer'),
    ('facebook',    '^https://((www|m|web)\.)?(facebook|fb)\.com/',                            'i-simple-icons-facebook'),
    ('canva',       '^https://((www\.)?canva\.com|([A-Za-z0-9-]+\.)+canva\.site)(/|$)',        'i-simple-icons-canva'),
    ('wordpress',   '^https://([A-Za-z0-9-]+\.)?wordpress\.(com|org)(/|$)',                    'i-simple-icons-wordpress'),
    ('shopify',     '^https://([A-Za-z0-9-]+\.)?(myshopify|shopify)\.com(/|$)',                'i-simple-icons-shopify'),
    ('notion',      '^https://(([A-Za-z0-9-]+\.)?notion\.site|(www\.)?notion\.(so|com))(/|$)', 'i-simple-icons-notion'),
    ('fiverr',      '^https://(www\.)?fiverr\.com/[A-Za-z0-9_]+',                              'i-simple-icons-fiverr');
