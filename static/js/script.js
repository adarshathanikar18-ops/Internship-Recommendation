function validateForm() {
  const cgpa = parseFloat(document.querySelector('input[name="cgpa"]').value);
  const prog = parseInt(document.querySelector('input[name="programming_score"]').value, 10);
  const subjectInputs = document.querySelectorAll('[data-subject-input]');

  if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
    alert('Please enter a valid CGPA between 0 and 10.');
    return false;
  }
  if (isNaN(prog) || prog < 0 || prog > 100) {
    alert('Please enter a valid programming score between 0 and 100.');
    return false;
  }
  for (const input of subjectInputs) {
    if (!input.value) continue;
    const score = parseInt(input.value, 10);
    if (isNaN(score) || score < 0 || score > 100) {
      alert('Subject marks should be between 0 and 100.');
      return false;
    }
  }
  return true;
}

document.querySelectorAll('[data-subject-input]').forEach(input => {
  input.addEventListener('input', function () {
    const value = parseInt(this.value, 10);
    if (value > 100) this.value = 100;
    if (value < 0) this.value = 0;
  });
});