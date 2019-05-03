import { AuthenticationContext, adalFetch, withAdalLogin } from 'react-adal';

// Configuration for Azure AD Tenant and Application
// TODO: Change these for training cluster
const tenant = '76648a49-7e8a-4b11-9aed-e3852b2f4295'
const clientId =  '265fd760-dbc8-4b6f-81bb-056197f24592'
const redirectUri = 'http://localhost:3000'

export const adalConfig = {
  tenant,
  clientId,
  endpoints: {
    api: `https://${tenant}/${clientId}`,
  },
  cacheLocation: 'localStorage',
  redirectUri
};

export const authContext = new AuthenticationContext(adalConfig);

export const adalApiFetch = (fetch, url, options) =>
  adalFetch(authContext, adalConfig.endpoints.api, fetch, url, options);

export const withAdalLoginApi = withAdalLogin(authContext, adalConfig.endpoints.api);