/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop-sarbani.us', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'JJNOXXXj5Tsth4j6VRe0j0chKeB6IdeF', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100/login-result', // the base url of the running ionic application. 
  }
};
