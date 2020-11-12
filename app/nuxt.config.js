require('dotenv').config()
import colors from 'vuetify/es5/util/colors'

export default {
    mode: 'universal',
    srcDir: 'src',

    watchers: {
        webpack: {
            poll: true
        }
    },

    /*
    ** Headers of the page
    */
    head: {
        titleTemplate: '%s - ' + process.env.npm_package_name,
        title: process.env.npm_package_name || '',
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
        ],
        link: [
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
        ]
    },
    /*
    ** Customize the progress-bar color
    */
    loading: { color: '#fff' },
    /*
    ** Global CSS
    */
    css: [
    ],
    /*
    ** Plugins to load before mounting the App
    */
    plugins: [
        {
            src: '@/plugins/vue-mavon-editor',
            ssr: false
        },
        { src: '~/plugins/day' }
    ],
    /*
    ** Nuxt.js dev-modules
    */
    buildModules: [
        '@nuxtjs/vuetify',
    ],
    /*
    ** Nuxt.js modules
    */
    modules: [
        '@nuxtjs/axios',
        '@nuxtjs/auth',
        ['@nuxtjs/dotenv', { filename: process.env.NODE_ENV !== 'production' ? "./configs/.env.dev" : "./configs/.env.prod" }
        ],
    ],
    axios: {
        // baseURL: process.env.BASE_URL,
        // browserBaseURL: process.env.BROWSER_BASE_URL,
        // credentials: true
        // proxyHeaders: false
    },
    auth: {
        redirect: {
            home: '/',
        },
        strategies: {
            local: {
                endpoints: {
                    login: { url: '/auth/token', method: 'post', propertyName: 'access_token', headers: { "Content-Type": "multipart/form-data" } },
                    user: { url: '/users/me/', method: 'get', propertyName: false },
                    logout: false
                }
            },
        }
    },
    router: {
        middleware: ['auth']
    },
    /*
    ** vuetify module configuration
    ** https://github.com/nuxt-community/vuetify-module
    */
    vuetify: {
        customVariables: ['~/assets/variables.scss'],
        theme: {
            dark: false,
            themes: {
                dark: {
                    primary: colors.blue.darken2,
                    accent: colors.grey.darken3,
                    secondary: colors.amber.darken3,
                    info: colors.teal.lighten1,
                    warning: colors.amber.base,
                    error: colors.deepOrange.accent4,
                    success: colors.green.accent3
                }
            }
        }
    },
    /*
    ** Build configuration
    */
    build: {
        /*
        ** You can extend webpack config here
        */
        extend(config, ctx) {
        }
    }
}
