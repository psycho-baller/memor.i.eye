export function isToday(date: Date): boolean {
  const today = new Date();

  if (
    today.getFullYear() === date.getFullYear() &&
    today.getMonth() === date.getMonth() &&
    today.getDate() === date.getDate()
  ) {
    return true;
  }

  return false;
}

export function isThisMonth(date: Date): boolean {
  const today = new Date();

  if (
    today.getFullYear() === date.getFullYear() &&
    today.getMonth() === date.getMonth()
  ) {
    return true;
  }

  return false;
}

export function isThisYear(date: Date): boolean {
  const today = new Date();

  if (today.getFullYear() === date.getFullYear()) {
    return true;
  }

  return false;
}