const { createApolloFetch } = require('apollo-fetch')

const wlGQL = require('./graphql')
const geo = require('./geo')
const property = require('./property')

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

async function updateEvent(context, tenantId, eventUpdate, suppressNotifications) {

  context.log(`Updating event - tenantId: ${tenantId}, id: ${eventUpdate.id}`)

  const variables = {
      tenantId,
      input: eventUpdate,
      eepConfig: {
        suppressNotifications
      }
  }

  const { data, errors } = await apolloFetch({ query: wlGQL.updateEventMutation, variables })

  if (errors) throw new Error(JSON.stringify(errors))

  if (data && data.event) {
    return data.event
  } 
  
  return null
}

module.exports = async function(context, eventHubMessages) {
  for (const message of eventHubMessages) {
    // context.log(`Processing message: ${JSON.stringify(message, null, 2)}`)  

    // Should also include additional filter logic here to stop multiple processing.
    // For example use agentId or a custom property flag/timestamp.
    if (message.itemType === "Event") {
      context.log(`Processing event - tenantId: ${message.tenantId}, id: ${message.itemId}`)

      const srcEvent = await getEventById(context, message.tenantId, message.itemId)

      // context.log( `Retrieved event: ${JSON.stringify(srcEvent, null, 2)}`)  

      const eventUpdate = {
        id: srcEvent.id
      }

      property.updateEventTopic(srcEvent, eventUpdate)
      geo.updateEventLocation(srcEvent, eventUpdate)

      // context.log( `Updated event: ${JSON.stringify(eventUpdate, null, 2)}`)  

      const result = await updateEvent(context, message.tenantId, eventUpdate, true)
    }
  }
}
