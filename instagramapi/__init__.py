import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from instagramapi.mixins.account import AccountMixin
from instagramapi.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from instagramapi.mixins.auth import LoginMixin
from instagramapi.mixins.bloks import BloksMixin
from instagramapi.mixins.challenge import ChallengeResolveMixin
from instagramapi.mixins.clip import DownloadClipMixin, UploadClipMixin
from instagramapi.mixins.collection import CollectionMixin
from instagramapi.mixins.comment import CommentMixin
from instagramapi.mixins.direct import DirectMixin
from instagramapi.mixins.explore import ExploreMixin
from instagramapi.mixins.fbsearch import FbSearchMixin
from instagramapi.mixins.fundraiser import FundraiserMixin
from instagramapi.mixins.hashtag import HashtagMixin
from instagramapi.mixins.highlight import HighlightMixin
from instagramapi.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from instagramapi.mixins.insights import InsightsMixin
from instagramapi.mixins.location import LocationMixin
from instagramapi.mixins.media import MediaMixin
from instagramapi.mixins.multiple_accounts import MultipleAccountsMixin
from instagramapi.mixins.note import NoteMixin
from instagramapi.mixins.notification import NotificationMixin
from instagramapi.mixins.password import PasswordMixin
from instagramapi.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from instagramapi.mixins.private import PrivateRequestMixin
from instagramapi.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from instagramapi.mixins.share import ShareMixin
from instagramapi.mixins.signup import SignUpMixin
from instagramapi.mixins.story import StoryMixin
from instagramapi.mixins.timeline import ReelsMixin
from instagramapi.mixins.totp import TOTPMixin
from instagramapi.mixins.track import TrackMixin
from instagramapi.mixins.user import UserMixin
from instagramapi.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("instagramapi")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    SignUpMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
