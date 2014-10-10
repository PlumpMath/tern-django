;;; tern-django-test.el --- tern-django test suite

;;; Commentary:

;;; Code:

(require 'ert)
(require 'tern-django)

(ert-deftest test-tern-django-run-command ()
  "Check we can run `tern-django' python script."
  (let ((tern-django-script "-V"))
    (tern-django)
    (should (tern-django-running-p))))

(ert-deftest test-tern-django-run-single-process-at-time ()
  "Check we run only one `tern-django' script instance."
  (let ((tern-django-process (start-process "cat" nil "cat")))
    (tern-django)
    (should (equal "cat" (car (process-command tern-django-process))))))

(ert-deftest test-tern-django-show-process-buffer-on-error ()
  "Check if `tern-django' show process output buffer on any error."
  (let ((tern-django-script "does_not_exist.py"))
    (tern-django)
    (wait-for-tern-django)
    (should (equal "*tern-django*" (buffer-name)))))

(ert-deftest test-tern-django-clean-output-buffer-for-each-run ()
  "Check that each `tern-django' script runs buffer contain its own output only."
  (let ((tern-django-script "-V"))
    (dotimes (i 2)
      (tern-django)
      (wait-for-tern-django))
    (with-current-buffer tern-django-buffer
      (should (equal (buffer-size)
                     (length "Python 3.4.0\n"))))))

(provide 'tern-django-test)

;;; tern-django-test.el ends here
