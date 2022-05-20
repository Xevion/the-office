module.exports = {
    root: true,
    env: {
        node: true
    },
    parserOptions: {
        parser: "babel-eslint",
    },
    extends: [
        'eslint:recommended',
        'plugin:vue/essential',
        'plugin:vue/recommended' // Use this if you are using Vue.js 2.x.
    ],
    rules: {
        // override/add rules settings here, such as:
        'vue/no-unused-vars': 'error',
        'indent': ['warn', 4],
        "vue/html-indent": ["error", 4, {
            "attribute": 1,
            "baseIndent": 1,
            "closeBracket": 0,
            "alignAttributesVertically": true,
            "ignores": []
        }],
        'vue/max-attributes-per-line': ["warn", {
            "singleline": {"max": 5},
            "multiline": {"max": 2}
        }]
    }
}
