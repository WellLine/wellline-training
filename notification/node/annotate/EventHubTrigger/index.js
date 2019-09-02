const { createApolloFetch } = require('apollo-fetch')

const wlGQL = require('./graphql')

const timeLineServiceUrl = process.env['TIMELINE_SVC_URL']
const authToken = process.env['TIMELINE_SVC_AUTH_TOKEN']

console.log(`TIMELINE_SVC_URL: ${timeLineServiceUrl}`)
// console.log(`TIMELINE_SVC_AUTH_TOKEN: ${authToken}`)

const apolloFetch = createApolloFetch({ uri: timeLineServiceUrl });

apolloFetch.use(({ request, options }, next) => {
  options.headers = {
    "authorization": `Bearer ${authToken}`
  }
  next()
})

async function getEventById(context, tenantId, eventId) {

  const variables = {
      tenantId,
      id: eventId,
      includeSystemEvents: true
  }

  const { data, errors, extensions } = await apolloFetch({ query: wlGQL.getEventQuery, variables })

  if (errors) throw new Error(JSON.stringify(errors))

  if (data && data.event) {
    return data.event
  } 
  
  return null
}

module.exports = async function(context, eventHubMessages) {
  for (const message of eventHubMessages) {
    if (message.itemType === "Event") {
      const event = await getEventById(context, message.tenantId, message.itemId)

      context.log(
        `Retrieved event: ${JSON.stringify(event, null, 2)}`
      )  
    }
  }
}
