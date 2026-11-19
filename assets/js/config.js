/* Home.Direct runtime configuration.
   The inbox address that receives every form, lead and pledge is stored here ENCODED
   (character codes, shifted and reversed) so it never appears as text anywhere on the site.
   - formAlias: after the first FormSubmit activation email arrives, FormSubmit gives you a
     random alias string. Paste it here to stop using the encoded address entirely.
   - paypalHostedButtonId: optional PayPal hosted "Donate" button ID. When set, donations use it
     instead of the encoded address.
*/
window.HD_CONFIG = {
  _k: [112,114,102,49,111,108,100,112,106,67,52,100,118,110,117,114,122,101,104,122],
  formAlias: "",
  paypalHostedButtonId: "",
  donateCurrency: "USD",
  siteName: "Home.Direct"
};
