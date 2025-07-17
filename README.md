# effective-mobile-junior

## installing

clone git

```bash
git clone https://github.com/mafooll/effective-mobile-junior.git
```

rename env.example -> .env && run from /effective-mobile-junior:

```bash
make makemigrations &&
make migrate &&
make createsuperuser &&
make
```

or

```bash
git clone https://github.com/mafooll/effective-mobile-junior.git &&
cd effective-mobile-junior &&
cp .env.example ./.env &&
make makemigrations &&
make migrate &&
make createsuperuser &&
make
```

## run tests

do that after make command in another terminal

```bash
make tests

```
