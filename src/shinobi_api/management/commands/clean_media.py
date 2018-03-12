#! /usr/bin/python
from django.core.management.base import BaseCommand
from shinobi_api.models.user_media import UserMedia
from shinobi_api.services import Utils
from shinobi_api.services.media import MediaService
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Oct 14th, 2016 2:59:07 PM$"

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        on_remove_medias = UserMedia.objects.filter(on_remove=1)
        remove_uris = []
        for _media in on_remove_medias:
            if _media.origin_uri:
                remove_uris.append(_media.origin_uri)
            if _media.thumb_uri:
                remove_uris.append(_media.thumb_uri)
            print ("**Removed: {0}**".format(_media.id))
            _media.delete()
        MediaService.clean_s3(remove_uris)
        print ("**Clean media: {0}**".format(len(remove_uris)))
        