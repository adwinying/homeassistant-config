#
# Change input source for TV
#

ENTITY     = 'media_player.room_tv'

MQTT_TOPIC_CMD    = 'cmnd/IR_Bridge/IRSEND'
MQTT_TOPIC_SOURCE = 'homeassistant/media_player/room_tv'

CMD_UP     = '{"Protocol":"NEC","Bits":32,"Data":"0x00FDB847"}'
CMD_DOWN   = '{"Protocol":"NEC","Bits":32,"Data":"0x00FDA25D"}'
CMD_ENTER  = '{"Protocol":"NEC","Bits":32,"Data":"0x00FD827D"}'
CMD_SOURCE = '{"Protocol":"NEC","Bits":32,"Data":"0x00FD7887"}'

SOURCES = (
    'HDMI1',
    'HDMI2',
    'HDMI3',
    'HDMI4',
)

STEP_COMMANDS = {
    -3: [CMD_SOURCE, CMD_UP, CMD_UP, CMD_UP, CMD_ENTER],
    -2: [CMD_SOURCE, CMD_UP, CMD_UP, CMD_ENTER],
    -1: [CMD_SOURCE, CMD_UP, CMD_ENTER],
    0: [],
    1: [CMD_SOURCE, CMD_DOWN, CMD_ENTER],
    2: [CMD_SOURCE, CMD_DOWN, CMD_DOWN, CMD_ENTER],
    3: [CMD_SOURCE, CMD_DOWN, CMD_DOWN, CMD_DOWN, CMD_ENTER],
}

def get_target_source():
    targetSource = data.get('source')

    if targetSource is None:
        raise Exception('[ERROR] source parameter is missing')

    return targetSource


def get_current_source():
    entityState = hass.states.get(ENTITY)

    if entityState is None:
        raise Exception('[ERROR] unable to get entity state')

    return entityState.attributes['source']


def send_command(topic, payload, retain = False):
    serviceData = { 'topic': topic, 'payload': payload, 'retain': retain }

    return hass.services.call('mqtt', 'publish', serviceData, True)


def set_source_state(source):
    payload = '{ "source": "%s" }' % source

    return send_command(MQTT_TOPIC_SOURCE, payload, True)

def main():
    targetSource  = get_target_source()
    currentSource = get_current_source()

    if (currentSource == 'unknown'):
        set_source_state(targetSource)
        raise Exception(f"[WARN] current source is unknown. Resetting source to target")

    targetIndex  = SOURCES.index(targetSource)
    currentIndex = SOURCES.index(currentSource)

    steps    = targetIndex - currentIndex
    commands = STEP_COMMANDS[steps]

    logger.debug(f"target: {targetIndex}, current: {currentIndex}, steps: {steps}")

    for command in commands:
        logger.debug(command)
        send_command(MQTT_TOPIC_CMD, command)

    set_source_state(targetSource)

main()
