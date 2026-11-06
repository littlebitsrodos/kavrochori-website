# Changelog

## 2026-11-06 — Χάρτης: tiles OpenStreetMap αντί για CARTO

Οι αλλαγές είναι σε κλάδο/PR. Το `main` και το live `https://kavrochori.gr` δεν πειράχτηκαν. Δεν αλλάζει DNS, Cloudflare, GitHub Pages ή οτιδήποτε live. Merge μόνο με νέο ρητό OK του Γιώργου.

### Γιατί

Στο live ο Leaflet φορτώνει (unpkg, HTTP 200), αλλά το CARTO Voyager

`https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png`

απαντά HTTP 200 με υδατογράφημα «API KEY REQUIRED» / carto.com/basemaps/apikey. Δρόμοι και ακτογραμμή δεν φαίνονται. Οι δείκτες και ο διακεκομμένος κύκλος μένουν. Δεν μπήκε κλειδί CARTO.

### Τι άλλαξε

Η πηγή είναι το `index.source.html`. Το `python3 sync_i18n.py` ξαναγράφει `/`, `/en/`, `/de/`, `/nl/`, `/he/`, `/fr/`.

Το layer είναι το ακριβές URL της πολιτικής tiles του OSMF:

`https://tile.openstreetmap.org/{z}/{x}/{y}.png`

Χωρίς `{s}`, χωρίς retina `{r}`, χωρίς API key. Το `maxZoom` μένει 19. Η απόδοση είναι «Leaflet | © OpenStreetMap contributors» (το «Leaflet» το προσθέτει η βιβλιοθήκη· ο σύνδεσμος πάει στο `openstreetmap.org/copyright`). Το CARTO έφυγε από την απόδοση.

Το CSP `img-src` είχε `https://*.basemaps.cartocdn.com` και `https://*.tile.openstreetmap.org`. Το wildcard δεν ταιριάζει στον host `tile.openstreetmap.org` χωρίς υποτομέα, που είναι το URL που ζητά η πολιτική. Το `img-src` έγινε `https://tile.openstreetmap.org`. Το `referrer` μένει `strict-origin-when-cross-origin`, ώστε ο browser να στέλνει Referer (origin της σελίδας), όπως ζητά η πολιτική, και να κρατά cache τα tiles. Ένας χάρτης αγγελίας, που φορτώνει μόνο όταν πλησιάζει η ενότητα, είναι η ελαφριά χρήση που επιτρέπει το `tile.openstreetmap.org`. Δεν γίνεται prefetch ούτε κατέβασμα για offline.

### Τι δεν άλλαξε

Κέντρο `[35.308, 25.047]`, zoom 12, κύκλος ακτίνας 3200 μ. με διακεκομμένη γραμμή, και οι δείκτες ΠΑΓΝΗ, ΙΤΕ / FORTH, Πανεπιστήμιο Κρήτης (συντεταγμένες και ετικέτες). Τιμή, φόρμα, `mailto:home@kavrochori.gr`, γλώσσες, JSON-LD. Το `sitemap.xml` είχε ήδη `lastmod` 2026-11-06.

## 2026-11-06 — Διορθώσεις από τον τεχνικό έλεγχο

Οι αλλαγές είναι σε κλάδο/PR. Το `main` και το live `https://kavrochori.gr` δεν πειράχτηκαν.

### Φόρμα επικοινωνίας

Η φόρμα εξακολουθεί να κάνει POST στο FormSubmit (`formsubmit.co`) προς `home@kavrochori.gr`. Το AJAX του FormSubmit δεν στέλνει `Access-Control-Allow-Origin` (έλεγχος GET από browser, χωρίς POST), οπότε δεν χρησιμοποιείται. Η υποβολή μένει στη σελίδα, μέσα σε πλαίσιο. Αν η υπηρεσία γυρίσει σφάλμα (όπως το 522 του ελέγχου), φαίνεται στο πλαίσιο και η σελίδα λέει ότι χωρίς επιβεβαίωση το μήνυμα δεν έφυγε. Ο σύνδεσμος `mailto:home@kavrochori.gr` είναι ορατός από πριν και, με JavaScript, παίρνει το κείμενο που γράφτηκε. Χωρίς JavaScript το πλαίσιο και το απλό mailto μένουν. Δεν προστέθηκε νέος επί πληρωμή πάροχος. Το CSP απέκτησε μόνο `frame-src https://formsubmit.co`, για αυτό το πλαίσιο.

### Εβραϊκά και skip link

Ο σύνδεσμος «μετάβαση στο περιεχόμενο» ήταν κρυμμένος με `left: -9999px`. Σε `dir="rtl"` αυτό φούσκωνε το οριζόντιο scroll (ίδιο και στο σημερινό `main`) και η αρχική όψη του `/he/` έβγαινε άδεια. Τώρα κρύβεται με `clip`, χωρίς αρνητικό `left`.

### Ένα H1 και μία γλώσσα ανά URL

Κάθε δημόσια σελίδα γλώσσας (`/`, `/en/`, `/de/`, `/nl/`, `/he/`, `/fr/`) έβγαζε και τις έξι γλώσσες και έξι `h1`. Η πηγή μένει το `index.source.html` (όλες οι γλώσσες). Το `python3 sync_i18n.py` γράφει τις δημόσιες σελίδες κρατώντας μόνο τη γλώσσα του URL, άρα ένα `h1`. Το αρχείο πηγής είναι `noindex` και μπλοκαρισμένο στο `robots.txt`, για να μην γίνει δεύτερη δημόσια αρχική.

### JSON-LD

Σε κάθε γλώσσα το `name`, το `description` και το `url` ακολουθούν τον τίτλο και το canonical της σελίδας. Προστέθηκε `Offer` με τιμή `610000` και νόμισμα `EUR`, ίδια με το 610.000 € που φαίνεται στη σελίδα. Δεν είναι αλλαγή τιμής.

### Hero

Η κεντρική φωτογραφία `dji-0128-800.webp` έχει περιγραφικό `alt` στη γλώσσα της σελίδας.

### Bitcoin

Έφυγε το WebSocket προς `stream.binance.com` (έδινε `ERR_CONNECTION_CLOSED` και ξαναδοκίμαζε). Η ισοτιμία δεν ζητιέται μόνη της στο φόρτωμα. Ο επισκέπτης μπορεί να πατήσει «Τιμή σε Bitcoin»· γίνεται μία κλήση REST και, αν αποτύχει, το κουμπί λέει ότι δεν είναι διαθέσιμη, χωρίς νέα προσπάθεια.

### Footer

Ο σύνδεσμος πολιτικής απορρήτου είναι υπογραμμισμένος και λευκός, ώστε να ξεχωρίζει από το γύρω κείμενο (Lighthouse `link-in-text-block`).

### Γραμματοσειρές

Η αρχική ονόμαζε Cormorant Garamond και DM Sans χωρίς να τις φορτώνει (το CSP δεν επιτρέπει Google Fonts). Η σελίδα απορρήτου τις φόρτωνε από Google. Αρχική, απόρρητο και 404 χρησιμοποιούν πλέον την ίδια στοίβα συστήματος (Georgia / system sans), χωρίς τρίτο πάροχο και χωρίς χαλάρωση του CSP. Τα `brochure.html` και `agency-pack.html` μένουν σε Google Fonts: είναι `noindex` φύλλα Α4, όχι η αγγελία, και δεν τα μετρά το Lighthouse της αρχικής.

### hreflang `en-IL`

Αφαιρέθηκε από το `<head>` και το sitemap. Έδειχνε στο ίδιο URL με το `en`, χωρίς ξεχωριστή σελίδα. Το κοινό από το Ισραήλ καλύπτεται από `/he/` (εβραϊκά) και `/en/` (αγγλικά).

### HTTP → HTTPS — χρειάζεται τον Γιώργο, δεν φτιάχνεται από το repo

Στον έλεγχο (6/11, ~14:00 ώρα Αθήνας) το `http://kavrochori.gr/` επέστρεφε HTTP 500 (Pingora) αντί για ανακατεύθυνση σε HTTPS.

Επανέλεγχος από αυτό το περιβάλλον στις 6/11/2026 ~13:05 UTC:

- `http://kavrochori.gr/` → **301** προς `https://kavrochori.gr/` (`server: GitHub.com`, Fastly/Varnish).
- `https://kavrochori.gr/` → 200.
- `https://www.kavrochori.gr/` → 301 προς την κορυφή.
- DNS: apex A `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (GitHub Pages). `www` CNAME `littlebitsrodos.github.io`. NS `dns1.papaki.gr` / `dns2.papaki.gr` (όχι Cloudflare).

Δεν υπάρχει αρχείο στο repo που να ορίζει τον ακροατή HTTP. Το GitHub Pages αγνοεί `_headers` και `_redirects`. Το `CNAME` είναι ήδη `kavrochori.gr`. Το `upgrade-insecure-requests` ισχύει μόνο αφού φορτώσει HTML, άρα δεν διορθώνει 500 στο HTTP.

**Μην αλλάξετε DNS, GitHub Pages ή domain μέχρι να το πει ρητά ο Γιώργος.** Αν το 500 ξαναεμφανιστεί: επιβεβαιώστε ότι στο GitHub → Settings → Pages το Enforce HTTPS είναι ανοιχτό, ότι τα A records μένουν οι διευθύνσεις του GitHub Pages και ότι δεν μπαίνει μπροστά Cloudflare proxy (το Pingora είναι proxy της Cloudflare). Μετά, `curl -sI http://kavrochori.gr/`.

### Cache στατικών — χρειάζεται τον Γιώργο, δεν φτιάχνεται από το repo

Το GitHub Pages / Fastly στέλνει `cache-control: max-age=600` και σε HTML και σε εικόνες. Δεν υπάρχει υποστηριζόμενο αρχείο headers σε αυτό το host· δεν προστέθηκε ψεύτικο `_headers`. Μεγαλύτερη cache θέλει CDN ή άλλη ρύθμιση μπροστά από το Pages, δηλαδή αλλαγή DNS/proxy. Αυτό δεν πρέπει να γίνει για χάρη του cache, και όχι πριν το ρητό OK του Γιώργου — ένας λάθος proxy είναι η πιθανή εξήγηση για το Pingora 500.
