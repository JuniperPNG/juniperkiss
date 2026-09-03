# Moving juniperkiss.com fully under your control

Goal: the website is built and published **only** from GitHub, and you never
have to log into Wix to keep it running.

---

## 1. Where things stand right now

You own the registration (bought through Wix), Wix runs the DNS, and Wix serves
the pages. Audited on this machine:

| Record | Current value | Meaning |
| --- | --- | --- |
| `juniperkiss.com` NS | `ns4.wixdns.net`, `ns5.wixdns.net` | **Wix controls your DNS zone** |
| `juniperkiss.com` A | `185.230.63.171`, `.186`, `.107` | Apex points at Wix's servers |
| `www.juniperkiss.com` CNAME | `cfd.wixdns.net` | www points at Wix via Cloudflare |

Two separate things are tangled together, and it helps to keep them apart:

1. **Registration** — who the registrar of record is. Currently Wix.
2. **DNS + hosting** — where the name resolves to and who serves the pages.
   Currently Wix.

You only *have* to change (2) for the GitHub site to go live. Changing (1) is
what removes Wix from your life permanently. Do them in that order.

---

## 2. Target configuration

| Record | Type | Value |
| --- | --- | --- |
| `juniperkiss.com` | A | `185.199.108.153` |
| `juniperkiss.com` | A | `185.199.109.153` |
| `juniperkiss.com` | A | `185.199.110.153` |
| `juniperkiss.com` | A | `185.199.111.153` |
| `juniperkiss.com` | AAAA | `2606:50c0:8000::153` |
| `juniperkiss.com` | AAAA | `2606:50c0:8001::153` |
| `juniperkiss.com` | AAAA | `2606:50c0:8002::153` |
| `juniperkiss.com` | AAAA | `2606:50c0:8003::153` |
| `www` | CNAME | `juniperpng.github.io` |
| `_github-pages-challenge-juniperpng` | TXT | *(value GitHub gives you — see step 4)* |

> Check the four A records against GitHub's current documented values before you
> paste them: **GitHub Docs → Pages → Managing a custom domain**. GitHub has
> changed them before and they are the one thing here that is not under your
> control.

Canonical hostname will be the apex, `https://juniperkiss.com`, matching
`_config.yml` and the `CNAME` file. GitHub will automatically redirect
`www.juniperkiss.com` to it.

---

## 3. ⚠️ Before you touch anything: check what else uses this domain

Changing nameservers replaces the **whole zone**, not just the website records.
If you have email on this domain, you will break it unless you copy the records
across.

In Wix, open **Domains → juniperkiss.com → Advanced → DNS records** and write
down (or screenshot) *everything*, especially:

- `MX` records — mail delivery. `hello@juniperkiss.com` is referenced on the
  new site, so something is presumably handling it.
- `TXT` records — SPF (`v=spf1 ...`), DKIM (`selector._domainkey`), DMARC
  (`_dmarc`). Missing these will silently send your outgoing mail to spam.
- Any `CNAME` used for verification by Google, Microsoft, or a mailbox provider.

Keep that list. You will re-enter every one of those records at the new DNS
host. **Only the A/AAAA/CNAME records for the website itself get changed.**

---

## 4. Prepare GitHub first (safe — changes nothing public)

1. **Repo → Settings → Pages.** Confirm *Source* is `Deploy from a branch`,
   branch `main`, folder `/`.
2. In **Custom domain**, enter `juniperkiss.com` and Save. It will show a red
   DNS error — expected, because DNS still points at Wix. Ignore it for now.
   This writes/refreshes the `CNAME` file in the repo.
3. **Verify the domain to prevent takeover.** Go to your GitHub *account*
   settings → **Pages** → **Add a domain**. GitHub gives you a TXT record named
   `_github-pages-challenge-juniperpng` with a token value. Note it down; you
   will add it in step 5. This stops anyone else ever claiming
   `juniperkiss.com` on GitHub Pages if a record is ever left dangling.
4. Leave **Enforce HTTPS** unticked for now; it cannot be enabled until the
   certificate is issued.

---

## 5. Point DNS at GitHub

Pick one route. **Route B is the recommendation**, because it gets your DNS out
of Wix immediately without waiting on any transfer lock.

### Route A — quickest: edit the records inside Wix

Keep Wix's nameservers, just change what they answer.

1. Wix → **Domains → juniperkiss.com → Advanced → DNS records**.
2. Delete the three Wix `A` records on the apex. Add the four GitHub `A`
   records and the four `AAAA` records.
3. Change the `www` `CNAME` from `cfd.wixdns.net` to `juniperpng.github.io`.
4. Add the `_github-pages-challenge-juniperpng` TXT record.
5. Leave MX and mail TXT records untouched.

*Pro:* five minutes, zero risk to email.
*Con:* Wix still controls the zone, and Wix has historically re-pointed records
when a Premium plan lapses. This is a stepping stone, not the destination.

### Route B — recommended: move the DNS zone to Cloudflare

1. Create a free Cloudflare account and **Add a site** → `juniperkiss.com`.
2. Cloudflare scans and imports your existing records. **Check the import
   against the list you made in step 3.** It misses records fairly often.
3. Set the website records to the target table above.
   - Set the proxy toggle (orange cloud) to **DNS only / grey** for the A, AAAA
     and `www` records. Let GitHub issue and serve its own certificate;
     proxying on top causes redirect loops and certificate errors.
4. Add the `_github-pages-challenge-juniperpng` TXT record.
5. Cloudflare gives you two nameservers, e.g. `xxx.ns.cloudflare.com`.
6. In Wix → **Domains → juniperkiss.com → Advanced → Nameservers**, switch from
   "Wix nameservers" to "External / custom" and enter Cloudflare's two.
7. Wait for propagation (usually under an hour, allow up to 48).

*Pro:* Wix is now only the registrar. It can no longer touch your website or
your mail. Free, and the same setup works from any future registrar.

### Route C — the end state: transfer the registration away from Wix

Do this **after** Route B is working, not before.

1. **Check the lock.** ICANN forbids transferring a domain within **60 days** of
   registration, of a previous transfer, or of a change of registrant contact.
   Wix will tell you if you are inside that window.
2. Wix → **Domains → juniperkiss.com → Advanced**:
   - Turn **off** domain lock / transfer lock.
   - Request the **authorisation code** (also called EPP code or transfer key).
     Wix emails it to the registrant address on file — make sure that address
     is one you can still read.
   - Turn **off** WHOIS privacy temporarily if the new registrar cannot read the
     contact email.
3. At the new registrar (Cloudflare Registrar is at-cost and has no upsells;
   Porkbun is a good alternative), start an **inbound transfer**, paste the auth
   code, and pay for the transfer year — this is added on top of your existing
   expiry, not wasted.
4. Approve the confirmation email. Transfers complete in about 5 days.
5. Because your nameservers are already Cloudflare's (Route B), **nothing about
   the website or email changes during the transfer**. That is the whole reason
   for doing B first.
6. Turn WHOIS privacy back on.

---

## 6. Turn on HTTPS and finish

Once DNS has propagated:

1. Repo → **Settings → Pages**. The custom domain should now show a green tick
   ("DNS check successful").
2. Wait for the Let's Encrypt certificate to be issued (minutes to an hour).
3. Tick **Enforce HTTPS**.
4. Visit `http://juniperkiss.com`, `https://www.juniperkiss.com` and
   `https://juniperkiss.com/post/mykindofamentor/` and confirm all three land on
   the HTTPS apex.

---

## 7. Only then, cancel Wix

Do **not** cancel until the checklist in section 8 is fully green, and give it a
week of the new site being live.

1. Wix → **Subscriptions**. Cancel the **Premium / Connect Domain** plan.
2. **Do not cancel the domain registration itself** and do not let it lapse —
   that is a different item, and if it expires you lose the name.
3. If you completed Route C, you can then close the Wix account entirely.
4. Export anything from Wix you have not already migrated. The 13 blog posts,
   39 images and 17 assignment PDFs in this repo are already copies of the
   originals, so the content itself is safe.

---

## 8. Verification checklist

Run these in PowerShell after each change.

```powershell
# Nameservers - should be Cloudflare (or Wix if you took Route A)
Resolve-DnsName juniperkiss.com -Type NS

# Apex - should be the four 185.199.x.153 addresses
Resolve-DnsName juniperkiss.com -Type A

# www - should be juniperpng.github.io
Resolve-DnsName www.juniperkiss.com -Type CNAME

# Domain verification token
Resolve-DnsName _github-pages-challenge-juniperpng.juniperkiss.com -Type TXT

# Mail must still resolve
Resolve-DnsName juniperkiss.com -Type MX

# End to end
Invoke-WebRequest https://juniperkiss.com -MaximumRedirection 0
```

- [ ] Old DNS list captured, including MX, SPF, DKIM, DMARC
- [ ] `CNAME` file in the repo contains `juniperkiss.com`
- [ ] GitHub account-level domain verification TXT record added and verified
- [ ] Apex resolves to GitHub's four A records
- [ ] `www` CNAMEs to `juniperpng.github.io` and redirects to the apex
- [ ] Certificate issued and **Enforce HTTPS** ticked
- [ ] `https://juniperkiss.com/post/mykindofamentor/` loads (old Wix URL shape)
- [ ] `https://juniperkiss.com/feed.xml` and `/sitemap.xml` load
- [ ] Test email sent **and received** at `hello@juniperkiss.com`
- [ ] A week has passed with no problems — *then* cancel the Wix plan

---

## 9. What "only maintained from GitHub" means afterwards

| Task | Where |
| --- | --- |
| Write a blog post | New file in `_posts/`, `git push` |
| Change the CV | Edit `_data/cv.yml`, `git push` |
| Add an assignment | Drop the PDF in `assets/documents/`, add an entry to `_data/assignments.yml` |
| Change the design | `assets/css/tokens.css` |
| Renew the domain | Registrar (Cloudflare/Porkbun after Route C), once a year — **turn on auto-renew** |
| Everything else | Nothing. There is no CMS, no plan, no monthly bill. |
