# coding: utf-8
from __future__ import unicode_literals
import pprint
import traceback

import youtube_dl
from twx.botapi import TelegramBot

__author__ = 'buyvich'


YDL_OPTS = {
    'outtmpl': '%(title)s-%(resolution)s.%(ext)s'
}


class YoutubeBot(object):

    api_token = ''

    def __init__(self):
        self.bot = TelegramBot(self.api_token)
        self.bot.get_me()
        last_updates = self.bot.get_updates(offset=0).wait()
        try:
            self.last_update_id = list(last_updates)[-1].update_id
        except IndexError:
            self.last_update_id = None
        print 'last update id: {}'.format(self.last_update_id)

    def process_message(self, message):

        text = message.message.text
        chat = message.message.chat
        text = text.strip().split('&')[0]
        msg = 'Could not download {}'.format(text)
        print 'Got message: \33[0;32m{}\33[0m'.format(text)
        try:
            self.bot.send_message(chat.id, 'Staring to download')
            with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
                r_code = ydl.download([text])
                if r_code == 0:
                    msg = '{} download successfully'.format(text)
        except Exception:
            pass
        self.bot.send_message(chat.id, msg)

    def run(self):
        print 'Main loop started'
        while True:
            updates = self.bot.get_updates(
                offset=self.last_update_id).wait()
            try:
                for update in updates:
                    if update.update_id > self.last_update_id:
                        pprint.pprint(update)
                        self.last_update_id = update.update_id
                        self.process_message(update)
            except Exception as ex:
                tb = traceback.format_exc()
                pprint.pprint(tb)


if __name__ == '__main__':
    try:
        YoutubeBot().run()
    except KeyboardInterrupt:
        print 'KeyboardInterrupt: exit'


# vim:ts=4:sts=4:sw=4:tw=85:et:
