# Abd_ru_shin_Books/settings.py

# ... (existing imports and other settings) ...

# Add the CMS-related apps to INSTALLED_APPS. Order is important!
INSTALLED_APPS = [
    'djangocms_admin_style', # Must be before 'django.contrib.admin'
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # IMPORTANT: Django CMS requires django.contrib.sites
    'cms', # Django CMS itself
    'menus', # Required for menu management
    'treebeard', # Required for tree structures
    'sekizai', # Required for JavaScript/CSS management
    'djangocms_text_ckeditor', # Rich text editor for CMS
    'djangocms_link', # Link plugin
    'djangocms_file', # File plugin
    'djangocms_picture', # Picture plugin
    'djangocms_video', # Video plugin
    'djangocms_snippet', # Snippet plugin
    'djangocms_style', # Style plugin
    'djangocms_googlemap', # Google Map plugin

    # Your existing apps
    'books',
    'crispy_forms',
    'crispy_bootstrap5',
]

# ... (existing MIDDLEWARE) ...
# Add CMS-related middleware. Order is crucial!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware', # For i18n
    'cms.middleware.utils.ApphookReloadMiddleware', # For apphooks (later)
    'cms.middleware.page.PageMiddleware', # Core CMS middleware
    'cms.middleware.user.UserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageMiddleware',
]

# ... (existing TEMPLATES configuration) ...
# CRITICAL: Add 'django.template.context_processors.request'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Add your project-level templates directory here if you have one
            # BASE_DIR / 'templates',
        ],
        'APP_DIRS': True, # Keep this True for app-specific templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # <-- ADD THIS ONE
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai', # <-- ADD THIS ONE
                'cms.context_processors.cms_settings', # <-- ADD THIS ONE
            ],
        },
    },
]

# ... (existing database, static files, etc.) ...

# REQUIRED: Add SITE_ID

# Also, ensure SITE_ID is defined (it's required by django.contrib.sites)
SITE_ID = 1 # Usually 1 unless you have specific multi-site setup

# ... and also ensure CMS_TEMPLATES is defined somewhere below INSTALLED_APPS.
# It must be present, even if empty, but I provided a basic one:
CMS_TEMPLATES = [
    ('fullwidth.html', 'Fullwidth Page'),
    ('home.html', 'Home Page (CMS)'),
]
# Media settings (CRITICAL for CMS - where uploaded files go)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # This will create a 'media' folder in your project root

# Optional: Configure STATIC_ROOT if you're going to collect static files for production
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Uncomment and manage for production

# Internationalization (i18n) settings (CRITICAL for CMS)
LANGUAGE_CODE = 'en' # Set your default language
USE_I18N = True
USE_L10N = True # For Django < 4.0, or use USE_TZ
USE_TZ = True # Recommended for Django >= 4.0

# Define the languages your CMS will support
LANGUAGES = [
    ('en', 'English'),
    # ('de', 'German'), # Example for another language
    # Add more languages as needed
]

CMS_LANGUAGES = {
    1: [ # SITE_ID 1
        {
            'code': 'en',
            'name': 'English',
            'fallbacks': ['en'],
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
        },
        # {
        #     'code': 'de',
        #     'name': 'German',
        #     'fallbacks': ['en'], # If German is not available, fallback to English
        #     'public': True,
        #     'redirect_on_fallback': True,
        #     'hide_untranslated': False,
        # },
    ],
    'default': {
        'fallbacks': ['en'],
        'redirect_on_fallback': True,
        'hide_untranslated': False,
        'public': True,
    }
}

# Define your CMS templates (can be changed later)
# These must be in your app's templates directory or project's templates directory
CMS_TEMPLATES = [
    ('fullwidth.html', 'Fullwidth Page'),
    ('home.html', 'Home Page (CMS)'), # You might want a specific CMS home template
    # Add more CMS-specific templates here
]

# CKEditor settings (for rich text editing in CMS)
CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'CMS',
    'skin': 'moono-lisa', # Or 'moono'
    ''width': '100%',
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['ShowBlocks'],
        ['Format', 'Styles'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
        ['Link', 'Unlink'],
        ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
        ['Source'],
    ],
}

# Other settings like LOGIN_REDIRECT_URL, CRISPY_TEMPLATE_PACK etc. remain the same
