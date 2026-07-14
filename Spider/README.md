# CyberSecurity_Pool
Package of exercices from 42School to learn basics in CyberSecurity

# Exercice I - Spider

The spider programm allow you to extract all the images from a website, recursively, by providing a url as a parameter.

### How to use it :

```
./Spider [-rlp] URL

    -r : recursively downloads the images in a URL received as a parameter

    -r -l [N]: indicates the maximum depth level of the recursive download. Default = 5

    -p [PATH] : indicates the path where the downloaded files will be saved. Default = ./data/

    -f : Change format to save (flat or based on original web storage)
```

The programm download the following extensions by default:
- .jpeg/.jpg
- .png
- .gif
- .bmp

### How the program works ?

###### First step : fetching the page

After verify all flags, we use the urllib librairy with .request and .urlopen() to fetching the page. Then we use read() to get the data and decode() to transform bytes data into Unicode string. This data, the html page structure is send into two functions "extract_images" and "extract_links"

###### Second step : Extract images and links

The html page is parsed with BeautifulSoup. "extract_images" looks for every `<img>` tag, resolves its `src` attribute into an absolute URL with `urljoin` (ignoring `data:` URIs), and keeps it only if it ends with one of the valid image extensions. "extract_links" looks for every `<a>` tag, resolves its `href` into an absolute URL, and keeps it only if it isn't an anchor/`mailto:`/`tel:` link, doesn't point to an image, and stays on the same domain (`netloc`) as the page it was found on. Both functions return a `set` so duplicate URLs found on the same page are discarded automatically.

###### Third step : Crawling and downloading

The crawl itself is a breadth-first search driven by a `deque` of `(url, depth)` pairs, starting with the URL given by the user at depth 0. For each URL popped from the queue, we skip it if it was already visited, otherwise we fetch the page and extract its images and links as described above. If the `-r` flag is set and the current depth is below the max level, every newly found link is pushed back onto the queue at `depth + 1`, which lets the crawler go deeper page after page. Every image found on the page is downloaded regardless of depth.

###### Fourth step : Saving files

"download_image" rebuilds a local file path from the image URL: with `-f` (flat mode) only the file's basename is kept, so every image lands directly in the destination folder; without it, the URL's path is reproduced under the destination folder, recreating the website's original directory structure. Missing folders are created on the fly with `os.makedirs`. The image is then fetched with `urllib.request.urlretrieve`; HTTP, URL and SSL errors are caught so one failed download doesn't stop the crawl.

### Error handling

- Invalid SSL certificates, malformed URLs, HTTP errors (404, 403, ...) and generic URL errors are all caught while fetching a page, printing an explicit message and moving on to the next URL in the queue instead of crashing.
- `-l` can only be used together with `-r` (checked at argument parsing time).
