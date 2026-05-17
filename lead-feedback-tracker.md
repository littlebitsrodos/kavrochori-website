# Lead Feedback Tracker — Kavrochori

Σκοπός: να μαθαίνουμε από την αγορά χωρίς να φτιάχνουμε άλλο ένα project.

Μην γράφετε πραγματικά ονόματα, email, τηλέφωνα ή προσωπικά στοιχεία μέσα σε αρχεία που θα γίνουν commit. Το `kavrochori` repo σερβίρεται από GitHub Pages, άρα ό,τι μπει εδώ μπορεί πρακτικά να δημοσιευτεί.

## Πού μπαίνουν τα πραγματικά leads

Χρησιμοποιήστε ένα από τα παρακάτω:

- Ένα ιδιωτικό spreadsheet εκτός repo.
- Το τοπικό αρχείο `../lead-feedback-private.csv`, που βρίσκεται εκτός του GitHub Pages repo.
- Εναλλακτικά, ένα τοπικό αρχείο `lead-feedback-private.csv` μέσα στο repo, που είναι ήδη στο `.gitignore`.

Το αρχείο `lead-feedback-template.csv` είναι μόνο template στηλών. Αν το χρησιμοποιήσετε τοπικά:

```bash
cp lead-feedback-template.csv ../lead-feedback-private.csv
```

## Στήλες

| Στήλη | Τι γράφουμε |
|---|---|
| `date` | Ημερομηνία πρώτης επαφής, π.χ. `2026-05-17`. |
| `source` | Από πού ήρθε: site, direct email, Spitogatos, idealista, broker, φίλος, άλλο. |
| `language` | Γλώσσα επικοινωνίας: EL, EN, DE, FR, NL, HE. |
| `buyer_type` | Οικογένεια, γιατρός/ερευνητής, expat, επενδυτής, broker, άγνωστο. |
| `inquiry_text_or_question` | Η βασική ερώτηση ή ανάγκη του αγοραστή, σύντομα. |
| `objection` | Τι τον κρατάει πίσω: τιμή, απόσταση, φωτογραφίες, financing, έγγραφα, άλλο. |
| `visit_requested` | `yes`, `no`, `maybe`. |
| `offer_or_price_signal` | Προσφορά, εύρος τιμής, σχόλιο τύπου "too high", ή κενό. |
| `follow_up_date` | Πότε πρέπει να ξαναγίνει επαφή. |
| `status` | Τρέχουσα κατάσταση από τη λίστα παρακάτω. |
| `next_action` | Το επόμενο συγκεκριμένο βήμα. |
| `notes` | Μόνο μη-ευαίσθητες παρατηρήσεις. |

## Status Values

Κρατήστε τα status λίγα:

- `new`
- `replied`
- `brochure_sent`
- `visit_proposed`
- `visit_booked`
- `visited`
- `offer_received`
- `not_fit`
- `closed`

## Εβδομαδιαία ανάγνωση

Κάθε εβδομάδα κοιτάμε μόνο αυτά:

- Πόσα σοβαρά inquiries ήρθαν;
- Από ποιο source ήρθαν;
- Ποια γλώσσα/αγορά δείχνει σημάδι ζωής;
- Ποιες αντιρρήσεις επαναλαμβάνονται;
- Ζήτησε κανείς επίσκεψη;
- Υπάρχει πραγματικό price signal ή μόνο περιέργεια;

Πρώτο γρήγορο διάβασμα: 2 εβδομάδες μετά την πρώτη πραγματική διανομή. Πιο χρήσιμο διάβασμα για τιμή/positioning: μετά από 4-6 εβδομάδες.
