# E-Mail-Vorlagen (Deutsch)

Supabase verschickt Bestätigungs- und Passwort-Mails standardmäßig auf Englisch. Diese Vorlagen ersetzen sie.

## So überträgst du sie

Supabase-Dashboard → **Authentication → Emails** (je nach Version auch **Email Templates**). Für jede Vorlage:

1. Den Reiter wählen (linke Spalte der Tabelle).
2. Bei **Subject** den Betreff einfügen.
3. Bei **Body** / **Message body** den kompletten Inhalt der HTML-Datei einfügen.
4. Speichern.

| Supabase-Vorlage | Betreff | Datei |
|---|---|---|
| Confirm signup | Bestätige deine E-Mail-Adresse für Arenly | [`01-confirm-signup.html`](01-confirm-signup.html) |
| Invite user | Du wurdest zu Arenly eingeladen | [`02-invite-user.html`](02-invite-user.html) |
| Magic link | Dein Anmeldelink für Arenly | [`03-magic-link.html`](03-magic-link.html) |
| Change email address | Bestätige deine neue E-Mail-Adresse | [`04-change-email.html`](04-change-email.html) |
| Reset password | Setze dein Arenly-Passwort zurück | [`05-reset-password.html`](05-reset-password.html) |
| Reauthentication | Dein Bestätigungscode für Arenly | [`06-reauthentication.html`](06-reauthentication.html) |

Für Arenly sind aktuell **Confirm signup** und **Reset password** wichtig, die anderen werden noch nicht genutzt. Mit allen sechs Vorlagen bleibt aber nirgends Englisch übrig.

## Platzhalter

Die Platzhalter in `{{ … }}` füllt Supabase beim Versand aus. Bitte nicht übersetzen oder verändern:

| Platzhalter | Bedeutung |
|---|---|
| `{{ .ConfirmationURL }}` | Bestätigungs- bzw. Anmeldelink |
| `{{ .Data.name }}` | Name aus der Registrierung; fehlt er, steht nur „Hallo,“ |
| `{{ .Email }}` / `{{ .NewEmail }}` | bisherige / neue E-Mail-Adresse |
| `{{ .Token }}` | 6-stelliger Code (nur Reauthentication) |

## Absender

Im kostenlosen Tarif kommen die Mails von Supabase selbst, und es gehen nur wenige Mails pro Stunde raus. Für den echten Betrieb unter **Authentication → Emails → SMTP Settings** einen eigenen Mail-Dienst eintragen (z. B. Resend oder Brevo). Dort lassen sich dann auch Absendername **Arenly** und eine eigene Absenderadresse (z. B. `noreply@arenly.app`) festlegen.
