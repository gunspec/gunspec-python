# gunspec/types/compat

Attachment compatibility: what fits a firearm, computed from mount interfaces and never from names. `__init__.py` re-exports everything, so `from gunspec.types.compat import X` is the import path; the split mirrors `packages/sdk/src/types/compat.ts`.

Governed by: [`../README.md`](../README.md).

| File | Purpose |
|---|---|
| `standards.py` | `InterfaceStandard`, `FirearmInterface`, platforms, `FirearmInterfaces`, `AttachmentManufacturer` |
| `attachments.py` | `Attachment`, `AttachmentDetail` (with `StandardRef`, `CaliberRating`, `provenance`), `FitVia`, `AttachmentFit` (with `source`), `FirearmAttachments`, `AttachmentFirearmFit`, `InterfaceFirearm` |
| `offers.py` | `OfferVendor`, `PublicOffer` |
| `params.py` | The TypedDict parameters for the compatibility endpoints |

Every enumerated field uses a `..vocabulary` Literal. `AttachmentManufacturer` lives in `standards.py` because both the attachment and the firearm-fit models name a `{id, name}` pair and the name predates the split.
