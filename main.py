import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def build_text_response(output_speech, should_end_session, session_attributes=None):
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output_speech
            },
            'shouldEndSession': should_end_session
        }
    }
    if session_attributes:
        response['sessionAttributes'] = session_attributes
    return response


def build_audio_response(audio_url):
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': '<speak><audio src="{}" /></speak>'.format(audio_url)
            },
            'shouldEndSession': True,
        }
    }
    return response


def get_welcome_response():
    output_speech = 'You can say simply, "play 7". The number can be between 1 and 100.'
    return build_text_response(output_speech, False)


def handle_session_end_request():
    output_speech = 'Have a nice day!'
    return build_text_response(output_speech, True)


def on_launch(request, session):
    logger.debug('request={}, session={}'.format(request, session))
    return get_welcome_response()


def play_particular(intent, session):
    conv_no = intent['slots']['conv_no']
    if 'value' not in conv_no:
        return get_welcome_response()
    conv_no = int(conv_no['value'])
    if conv_no >= 0 and conv_no <= 100:
        return build_audio_response('https://s3.amazonaws.com/eng-conv-skill/DAY{:03d}.mp3'.format(conv_no))
    else:
        return get_welcome_response()


def play_random(intent, session):
    return get_welcome_response()


def on_intent(request, session):
    logger.debug('request={}, session={}'.format(request, session))
    intent = request['intent']
    intent_name = request['intent']['name']

    if intent_name == 'AMAZON.HelpIntent':
        return get_welcome_response()
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    elif intent_name == 'PlayParticular':
        return play_particular(intent, session)
    elif intent_name == 'PlayRandom':
        return play_random(intent, session)
    else:
        raise ValueError('Invalid intent')


def lambda_handler(event, context):
    request = event['request']
    request_type = request['type']
    session = event['session']

    if request_type == 'LaunchRequest':
        formatter = logging.Formatter('{} %(filename)s:%(lineno)d %(funcName)s() %(message)s\n'.format(request_type), '%H:%M:%S')
        logger.handlers[0].setFormatter(formatter)
        return on_launch(request, session)
    elif request_type == 'IntentRequest':
        intent_name = request['intent']['name']
        formatter = logging.Formatter('{} %(filename)s:%(lineno)d %(funcName)s() %(message)s\n'.format(intent_name), '%H:%M:%S')
        logger.handlers[0].setFormatter(formatter)
        return on_intent(request, session)
