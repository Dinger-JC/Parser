# Parser Industry-Hardstyle-Sex
:)

## About the project
A parser of videos from porn sites. Downloads videos only in the best quality. Beginning of development 06.01.2026.

## Getting Started
Before starting the project, you need to do the following:

### Installation
1. Libraries for the correct operation of the project:
   - ```shell
      pip install curl_cffi bs4 yt_dlp ffmpeg-python
       ```
2. Programs for downloading videos correctly:
    - `https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45`

### Create
Create a `data.json` file and write the following code. Then add your links to the `videos` dictionary:
```json
{
  "sites":
    {
      "AnalMedia": "anal.media",
      "Strip2": "vps402.strip2.co"
    },
  "videos":
    {
      "1": "https://vps402.strip2.co/video/...",
      "2": "https://anal.media/ru/video/..."
    }
}
```

## Roadmap
- [x] Add change log
- [x] Add link verification
- [ ] Add support other sites
- [ ] Add GUI
