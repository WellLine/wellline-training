module.exports.updateEventTopic = function(srcEvent, eventUpdate) {
    eventUpdate.addProperties = [{ name:"topic", "value": `allen - ${srcEvent.startedOn}` }]
}
  