#----------------------------------------------------------------------

    # Libraries
from enum import Enum
from typing import Generator
#----------------------------------------------------------------------

    # Class
class QFiles:
    class Dialog(Enum):
        OpenFileName = 0
        OpenFileNames = 1
        OpenFileUrl = 2
        OpenFileUrls = 3
        SaveFileName = 4
        SaveFileUrl = 5
        ExistingDirectory = 6
        ExistingDirectoryUrl = 7

    class Extension:
        class Image(Enum):
            def all(title: str = '') -> str:
                return QFiles.Extension.combine_single(title, *(ext.value for ext in QFiles.Extension.Image))

            def get() -> Generator:
                return (ext.value for ext in QFiles.Extension.Image)

            BMP = 'BMP (*.bmp *.dib *.rle)'
            CUR = 'CUR (*.cur)'
            GIF = 'GIF (*.gif)'
            ICNS = 'ICNS (*.icns)'
            ICO = 'ICO (*.ico)'
            JPEG = 'JPEG (*.jpeg *.jpg)'
            PBM = 'PBM (*.pbm)'
            PGM = 'PGM (*.pgm)'
            PNG = 'PNG (*.png)'
            PPM = 'PPM (*.ppm)'
            SVG = 'SVG (*.svg *.svgz)'
            TGA = 'TGA (.tga)'
            TIFF = 'TIFF (*.tif *.tiff)'
            WBMP = 'WBMP (*.wbmp)'
            WEBP = 'WEBP (*.webp)'
            XBM = 'XBM (*.xbm)'
            XPM = 'XPM (*.xpm)'
            HEIC = 'HEIC (*.heic)'
            JPEGXR = 'JPEG XR (*.jxr *.wdp *.wmp)'
            DDS = 'Surface DirectDraw (*.dds)'

        class Audio(Enum):
            def all(title: str = '') -> str:
                return QFiles.Extension.combine_single(title, *(ext.value for ext in QFiles.Extension.Audio))

            def get() -> Generator:
                return (ext.value for ext in QFiles.Extension.Audio)

            # RIFF = 'RIFF (*.riff)'
            # BWF = 'BWF (*.bwf)'
            # CAF = 'CAF (*.caf)'
            # AC3 = 'AC-3 (*.ac3)'
            # VQF = 'VQF / TwinVQ (*.vqf *.vql *.vqe)'
            # ASF = 'ASF (*.asf)'
            # ATRAC = 'ATRAC (*.aa3 *.oma *.at3)'
            _3GP = '3GP (*.3gp)'
            AA = 'AA (*.aa)'
            AAC = 'AAC (*.aac)'
            AAX = 'AAX (*.aax)'
            ACT = 'ACT (*.act)'
            AIFF = 'AIFF (*.aiff)'
            ALAC = 'ALAC (*.alac)'
            AMR = 'AMR (*.amr)'
            APE = 'APE (*.ape)'
            AU = 'AU (*.au)'
            AWB = 'AWB (*.awb)'
            DSS = 'DSS (*.dss)'
            DVF = 'DVF (*.dvf)'
            FLAC = 'FLAC (*.flac)'
            GSM = 'GSM (*.gsm)'
            IKLAX = 'IKLAX (*.iklax)'
            IVS = 'IVS (*.ivs)'
            M4A = 'M4A (*.m4a)'
            M4B = 'M4B (*.m4b)'
            M4P = 'M4P (*.m4p)'
            MMF = 'MMF (*.mmf)'
            MP3 = 'MP3 (*.mp3)'
            MPC = 'MPC (*.mpc)'
            MSV = 'MSV (*.msv)'
            NMF = 'NMF (*.nmf)'
            OGG = 'OGG (*.ogg *.oga *.mogg)'
            OPUS = 'OPUS (*.opus)'
            RA = 'RA (*.ra *.rm)'
            RAW = 'RAW (*.raw)'
            RF64 = 'RF64 (*.rf64)'
            SLN = 'SLN (*.sln)'
            TTA = 'TTA (*.tta)'
            VOC = 'VOC (*.voc)'
            VOX = 'VOX (*.vox)'
            WAV = 'WAV (*.wav)'
            WMA = 'WMA (*.wma)'
            WV = 'WV (*.wv)'
            WEBM = 'WEBM (*.webm)'
            _8SVX = '8SVX (*.8svx)'
            CDA = 'CDA (*.cda)'

        class Video(Enum):
            def all(title: str = '') -> str:
                return QFiles.Extension.combine_single(title, *(ext.value for ext in QFiles.Extension.Video))
            
            def get() -> Generator:
                return (ext.value for ext in QFiles.Extension.Video)

            WEBM = 'WebM (*.webm)'
            MKV = 'Matroska (*.mkv)'
            FLV = 'Flash Video (*.flv *.f4v *.f4p *.f4a *.f4b)'
            VOB = 'Vob (*.vob)'
            OGG = 'Ogg Video (*.ogv *.ogg)'
            DRC = 'Dirac (*.drc)'
            GIF = 'GIF (*.gif)'
            GIFV = 'Video alternative to GIF (*.gifv)'
            MNG = 'Multiple-image Network Graphics (*.mng)'
            AVI = 'AVI (*.avi)'
            MPEG = 'MPEG Transport Stream (*.mts *.m2ts *.ts)'
            MOV = 'QuickTime File Format (*.mov *.qt)'
            WMV = 'Windows Media Video (*.wmv)'
            YUV = 'Raw video format (*.yuv)'
            RM = 'RealMedia (*.rm)'
            RMVB = 'RealMedia Variable Bitrate (*.rmvb)'
            VIV = 'VivoActive (*.viv)'
            ASF = 'Advanced Systems Format (*.asf)'
            AMV = 'AMV video format (*.amv)'
            MP4 = 'MPEG-4 Part 14 (*.mp4 *.m4p *.m4v)'
            MPEG1 = 'MPEG-1 (*.mpg *.mp2 *.mpeg *.mpe *.mpv)'
            MPEG2 = 'MPEG-2 – Video (*.mpg *.mpeg *.m2v)'
            M4V = 'M4V (*.m4v)'
            SVI = 'SVI (*.svi)'
            _3GP = '3GPP (*.3gp)'
            _3G2 = '3GPP2 (*.3g2)'
            MXF = 'Material Exchange Format (*.mxf)'
            ROQ = 'ROQ (*.roq)'
            NSV = 'Nullsoft Streaming Video (*.nsv)'



        def combine(*extensions: Image|Audio|Video) -> str:
            return ';;'.join(list(ext.value for ext in extensions))

        def combine_single(title: str = '', *extensions: Image|Audio|Video) -> str:
            extStr = ''
            for ext in extensions:
                extStr += ext.value.split('(')[-1][:-1] + ' '
            extStr = extStr[:-1]

            return f'{title} ({extStr})'

        def combine_all(title: str = '', *extensions: Image|Audio|Video) -> str:
            if len(extensions) > 1:
                return QFiles.Extension.combine_single(title, *extensions) + ';;' + QFiles.Extension.combine(*extensions)
            return QFiles.Extension.combine_single(title, *extensions)

        def combine_by_category(category: Image|Audio|Video):
            return ';;'.join(list(ext.value for ext in category))

        def combine_by_category_all(title: str = '', category: Image|Audio|Video = None) -> str:
            if not category: return ''
            return QFiles.Extension.combine_single(title, *(ext for ext in category)) + ';;' + QFiles.Extension.combine_by_category(category)
#----------------------------------------------------------------------
