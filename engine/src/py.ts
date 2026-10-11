/** Emulazione dei dettagli numerici di Python che contano per la parità:
 *  round() e il formato f"{x:.nf}" arrotondano "half to even" sul valore binario
 *  esatto, mentre toFixed() di JS arrotonda i pareggi verso l'alto. */

/** f"{x:.nf}" di Python. */
export function pyFixed(x: number, nd: number): string {
  if (!isFinite(x)) return String(x);
  const neg = x < 0 || Object.is(x, -0);
  const s = Math.abs(x).toFixed(Math.min(100, nd + 30)); // espansione esatta
  const [int, frac] = s.split(".");
  const keep = frac.slice(0, nd);
  const rest = frac.slice(nd);
  let up = false;
  if (rest[0] > "5") up = true;
  else if (rest[0] === "5") {
    if (/[1-9]/.test(rest.slice(1))) up = true;
    else {
      // pareggio esatto: verso la cifra pari
      const last = nd > 0 ? keep[nd - 1] : int[int.length - 1];
      up = Number(last) % 2 === 1;
    }
  }
  let digits = int + keep;
  if (up) {
    // incrementa la stringa decimale
    const arr = digits.split("");
    let i = arr.length - 1;
    while (i >= 0) {
      if (arr[i] === "9") { arr[i] = "0"; i--; }
      else { arr[i] = String(Number(arr[i]) + 1); break; }
    }
    if (i < 0) arr.unshift("1");
    digits = arr.join("");
  }
  const ip = digits.slice(0, digits.length - nd) || "0";
  const fp = digits.slice(digits.length - nd);
  const out = nd > 0 ? `${ip}.${fp}` : ip;
  return (neg && /[1-9]/.test(out) ? "-" : "") + out;
}

/** round(x, nd) di Python. */
export function pyRound(x: number, nd: number): number {
  return Number(pyFixed(x, nd));
}

/** Confronto di tuple alla Python (lessicografico, numeri). */
export function cmpTuple(a: number[], b: number[]): number {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] < b[i]) return -1;
    if (a[i] > b[i]) return 1;
  }
  return a.length - b.length;
}
