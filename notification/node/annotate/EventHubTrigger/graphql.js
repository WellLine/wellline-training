const gql = require('graphql-tag')

//
// GQL Fragments
//
const EventDetailsFragment = gql`
  fragment EventDetails on Event {
    id
    externalId
    type {
      id
      name
    }
    batchId
    source {
      id
      name
    }
    startedOn
    startedAt {
      lat
      long
    }
    endedOn
    endedAt {
      lat
      long
    }
    content
    summary
    subjectEntityIds
    referenceEntityIds
    sourceEventIds
    createdOn
    createdBy {
      id
    }
    measures {
      type {
        id
        name
        units
      }
      value
    }
    quantities {
      unit
      value
    }
    properties {
      name
      value
    }
    links {
      uri
      description
      typeId
    }
  }
`

//
// GQL Queries
//
module.exports.getEventQuery = gql`
  query event($tenantId: ID!, $id: ID!, $includeSystemEvents: Boolean) {
    event(tenantId: $tenantId, id: $id, includeSystemEvents: $includeSystemEvents) {
      ...EventDetails
    }
  }
  ${EventDetailsFragment}
`
