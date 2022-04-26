{
  'includes': [ 'common-sqlite.gypi' ],

  'target_defaults': {
    'default_configuration': 'Release',
    'cflags':[
      '-std=c99'
    ],
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 1, # static debug
          },
        },
      },
      'Release': {
        'defines': [ 'NDEBUG' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 0, # static release
          },
        },
      }
    },
    'msvs_settings': {
      'VCCLCompilerTool': {
      },
      'VCLibrarianTool': {
      },
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
      },
    },
    'conditions': [
      ['OS == "win"', {
        'defines': [
          'WIN32'
        ],
        'conditions': [
          ['target_arch == "ia32"', {
            'variables': {
              'openssl_root%': 'OpenSSL-Win32',
              'icu_root%': 'icu_x86-windows',
            }
          }, 'target_arch == "arm64"', {
            'variables': {
              'openssl_root%': 'OpenSSL-Win64-ARM',
            }
          }, {
            'variables': {
              'openssl_root%': 'OpenSSL-Win64',
              'icu_root%': 'icu_x64-windows',
            }
          }]
        ],
        'link_settings': {
          'libraries': [
            '-llibcrypto.lib',
            '-llibssl.lib',
            # The two libs below are needed for the Electron build to succeed
            '-lws2_32.lib',
            '-lcrypt32.lib',
            '-licuuc.lib',
            '-licuin.lib',
          ],
          'library_dirs': [
            '<(module_root_dir)/deps/<(openssl_root)',
            '<(module_root_dir)/deps/<(icu_root)',
          ]
        }
      },
      'OS == "mac"', {
        'link_settings': {
          'libraries': [
            # This statically links libcrypto, whereas -lcrypto would dynamically link it
            '<(module_root_dir)/deps/openssl-macos/libcrypto.a'
          ]
        }
      },
      { # Linux
        'link_settings': {
          'libraries': [
            '-lcrypto'
          ]
        }
      }]
    ],
  },

  'targets': [
    {
      'target_name': 'sqlite3',
      'type': 'static_library',
      "conditions": [
        ["OS == \"win\"", {
          'include_dirs': [
            './sqlcipher-amalgamation/',
            './openssl-include/',
            './fts/',
            './icu_include/',
          ]
        },
        "OS == \"mac\"", {
          'include_dirs': [
            './sqlcipher-amalgamation/',
            './openssl-include/'
          ]
        },
        { # linux
          'include_dirs': [
            './sqlcipher-amalgamation/'
          ]
        }]
      ],
      'sources': [
        './sqlcipher-amalgamation/sqlite3.c'
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          './sqlcipher-amalgamation/'
        ],
        'defines': [
          'SQLITE_THREADSAFE=1',
          'HAVE_USLEEP=1',
          'SQLITE_ENABLE_FTS3',
          'SQLITE_ENABLE_FTS5',
          'SQLITE_ENABLE_JSON1',
          'SQLITE_ENABLE_RTREE',
          'SQLITE_HAS_CODEC',
          'SQLITE_TEMP_STORE=2',
          'SQLITE_SECURE_DELETE',
          'SQLITE_ENABLE_DBSTAT_VTAB=1',
          'ENABLE_MMICU',
        ],
      },
      'cflags_cc': [
          '-Wno-unused-value'
      ],
      'defines': [
        '_REENTRANT=1',
        'SQLITE_THREADSAFE=1',
        'HAVE_USLEEP=1',
        'SQLITE_ENABLE_FTS3',
        'SQLITE_ENABLE_FTS5',
        'SQLITE_ENABLE_JSON1',
        'SQLITE_ENABLE_RTREE',
        'SQLITE_HAS_CODEC',
        'SQLITE_TEMP_STORE=2',
        'SQLITE_SECURE_DELETE',
        'SQLITE_ENABLE_DBSTAT_VTAB=1',
        'ENABLE_MMICU',
      ]
    }
  ]
}
