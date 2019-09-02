module.exports.updateEventLocation = function(srcEvent, eventUpdate) {

    if (!srcEvent.startedAt 
      && srcEvent.subjectEntityIds 
      && srcEvent.subjectEntityIds.length > 0 
      && srcEvent.subjectEntityIds[0].startsWith("well.")) {
  
      const wellId = srcEvent.subjectEntityIds[0]
  
      if (wellId.startsWith("well.NO 15/9-F-15")) {
        eventUpdate.startedAt = { lat: 58.441585, long: 1.887541}
        eventUpdate.endedAt = { lat: 58.441585, long: 1.887541}
      } else if (wellId.startsWith("well.NO 15/9-F-14")) {
        eventUpdate.startedAt = { lat: 58.441602, long: 1.887522}
        eventUpdate.endedAt = { lat: 58.441602, long: 1.887522}
      } else if (wellId.startsWith("well.NO 15/9-F-13")) {
        eventUpdate.startedAt = { lat: 58.44162, long: 1.887502}
        eventUpdate.endedAt = { lat: 58.44162, long: 1.887502}
      } else if (wellId.startsWith("well.NO 15/9-F-12")) {
        eventUpdate.startedAt = { lat: 58.441637, long: 1.887483}
        eventUpdate.endedAt = { lat: 58.441637, long: 1.887483}
      } else if (wellId.startsWith("well.NO 15/9-F-11")) {
        eventUpdate.startedAt = { lat: 58.441654, long: 1.887463}
        eventUpdate.endedAt = { lat: 58.441654, long: 1.887463}
      } else if (wellId.startsWith("well.NO 15/9-F-10")) {
        eventUpdate.startedAt = { lat: 58.441578, long: 1.887519}
        eventUpdate.endedAt = { lat: 58.441578, long: 1.887519}
      } else if (wellId.startsWith("well.NO 15/9-F-9")) {
        eventUpdate.startedAt = { lat: 58.441596, long: 1.8875}
        eventUpdate.endedAt = { lat: 58.441596, long: 1.8875}
      } else if (wellId.startsWith("well.NO 15/9-F-8")) {
        eventUpdate.startedAt = { lat: 58.441613, long: 1.88748}
        eventUpdate.endedAt = { lat: 58.441613, long: 1.88748}
      } else if (wellId.startsWith("well.NO 15/9-F-6")) {
        eventUpdate.startedAt = { lat: 58.441648, long: 1.887441}
        eventUpdate.endedAt = { lat: 58.441648, long: 1.887441}
      } else if (wellId.startsWith("well.NO 15/9-F-5")) {
        eventUpdate.startedAt = { lat: 58.441571, long: 1.887497}
        eventUpdate.endedAt = { lat: 58.441571, long: 1.887497}
      } else if (wellId.startsWith("well.NO 15/9-F-4")) {
        eventUpdate.startedAt = { lat: 58.441589, long: 1.887478}
        eventUpdate.endedAt = { lat: 58.441589, long: 1.887478}
      } else if (wellId.startsWith("well.NO 15/9-F-3")) {
        eventUpdate.startedAt = { lat: 58.441606, long: 1.887458}
        eventUpdate.endedAt = { lat: 58.441606, long: 1.887458}
      } else if (wellId.startsWith("well.NO 15/9-F-2")) {
        eventUpdate.startedAt = { lat: 58.441623, long: 1.884661}
        eventUpdate.endedAt = { lat: 58.441623, long: 1.884661}
      } else if (wellId.startsWith("well.NO 15/9-F-1")) {
        eventUpdate.startedAt = { lat: 58.441641, long: 1.887419}
        eventUpdate.endedAt = { lat: 58.441641, long: 1.887419}
      }
    }
  }