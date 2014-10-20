;;; tern-django-test.el --- tern-django test suite

;;; Commentary:

;;; Code:

(require 'ert)
(require 'tern-django)

(ert-deftest test-tern-django-run-command ()
  "Check we can run `tern-django' python script."
  (unwind-protect
      (let ((tern-django-script "-i"))
        (tern-django)
        (should (tern-django-running-p)))
    (tern-django-terminate)))

(ert-deftest test-tern-django-dont-run-command-outside-django ()
  "We will start process only in django environment."
  (unwind-protect
      (let (process-environment)
        (tern-django)
        (should-not (tern-django-running-p)))
    (tern-django-terminate)))

(ert-deftest test-tern-django-run-single-process-at-time ()
  "Check we run only one `tern-django' script instance."
  (unwind-protect
      (let ((tern-django-process (start-process "cat" nil "cat")))
        (tern-django)
        (should (equal "cat" (car (process-command tern-django-process)))))
    (tern-django-terminate)))

(ert-deftest test-tern-django-show-process-buffer-on-error ()
  "Check if `tern-django' show process output buffer on any error."
  (unwind-protect
      (let ((tern-django-script "does_not_exist.py"))
        (tern-django)
        (wait-for-tern-django)
        (should (equal "*tern-django*" (buffer-name))))
    (tern-django-terminate)))

(ert-deftest test-tern-django-clean-output-buffer-for-each-run ()
  "Check that each `tern-django' script runs buffer contain its own output only."
  (unwind-protect
      (let ((tern-django-script "-V"))
        (with-current-buffer (get-buffer-create tern-django-buffer)
          (erase-buffer)
          (insert "Trash content...")
          (tern-django)
          (wait-for-tern-django)
          (goto-char (point-min))
          (should-not (looking-at-p "Trash content..."))))
    (tern-django-terminate)))

(provide 'tern-django-test)

;;; tern-django-test.el ends here
