const HtmlWebPackPlugin = require("html-webpack-plugin");
const path = require("path");
module.exports = {
  devtool: "source-map",
  output: {
    path: path.join(__dirname, "dist")
  },
  resolve: {
    extensions: [".wasm", ".mjs", ".js", ".json", ".jsx"]
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ["babel-loader"]
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader",
            options: { minimize: true }
          }
        ]
      },
      {
        test: /\.(gif|svg|jpg|png|ico)$/,
        loader: "file-loader"
      }
    ]
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: "./src/index.html",
      filename: "./index.html",
      favicon: "src/images/favicon.ico"
    })
  ],
  devServer: {
    open: false,
    hot: true,
    historyApiFallback: true,
    proxy: {
      "/V1/stations": {
        target: "http://localhost",
        changeOrigin: true
      }
    }
  }
};
