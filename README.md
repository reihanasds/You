# Irisan vertikal agen pemasaran Kim Holiday

Repositori ini berisi pipeline pemasaran lokal khusus draf untuk Kim Holiday. Alurnya mengikuti pola agen spesialis—**orchestrator → content strategist → Instagram curator → brand guardian → anti-slop reviewer → draf JSON tervalidasi**—tanpa memerlukan API key. Teks yang dihasilkan untuk pengguna ditulis dalam Bahasa Indonesia.

```bash
PYTHONPATH=src python -m kim_holiday "questions to ask before planning"
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m kim_holiday.api
```

Penyedia deterministik adalah default yang dapat diuji. Adapter LLM di masa depan dapat mengimplementasikan `ContentProvider` di `src/kim_holiday/provider.py`, sementara ledger bukti di `knowledge/kim-holiday-business-facts.json` tetap menjadi sumber kebenaran. Harga, ketersediaan, kapasitas, dan testimoni yang belum diketahui tidak pernah diisi. Setiap keluaran berstatus `draft` dengan `approval_required: true`; tidak ada yang dipublikasikan.

## API draf

API lokal berjalan pada port 8080 dan menyediakan `GET /health` serta `POST /draft`. Endpoint draf menerima `{"topic":"..."}` dan mengembalikan JSON tervalidasi.

```bash
PYTHONPATH=src python -m kim_holiday.api
curl http://127.0.0.1:8080/health
curl --header 'Content-Type: application/json' \
  --data '{"topic":"questions to ask before planning"}' \
  http://127.0.0.1:8080/draft
docker build -t kim-holiday-draft-api .
docker run --rm -p 8080:8080 kim-holiday-draft-api
```

See [workflows/content-draft.md](workflows/content-draft.md) for the workflow and [CI.md](CI.md) for repository validation.

## Uji coba draf tiga hari

GitHub Actions dapat menjalankan agen deterministik sekali sehari selama tiga hari kalender UTC. Workflow hanya mengunggah artefak draf JSON; tidak pernah mempublikasikan atau melakukan deployment.

1. Buka **Actions → Kim Holiday 3-day draft trial → Run workflow**, atur `start_date` (`YYYY-MM-DD`) bila perlu, lalu jalankan sekali.
2. Pantau run workflow dan artefak yang dibuat pada ringkasan run. Run terjadwal berlangsung pukul 00:15 UTC.
3. Unduh artefak bernama `kim-holiday-draft-day-<day>-<run-id>` dari setiap run yang berhasil.
4. Hentikan lebih awal dengan menonaktifkan workflow di UI Actions, atau hapus jadwal setelah uji coba. Run di luar jendela tiga hari akan berhenti dengan notifikasi.

Setiap artefak berisi `run_metadata`, label bukti, `approval_required: true`, dan `publication: "dinonaktifkan"`. Persetujuan manusia tetap wajib dan tidak ada jalur auto-publish.
