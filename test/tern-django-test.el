;;; tern-django-test.el --- tern-django test suite

;;; Commentary:

;;; Code:

(require 'ert)
(require 'tern-django)

(ert-deftest test-tern-django-run-command ()
  "Check we can run `tern-django' python script."
  (let ((tenr-django-script "-V"))
    (tern-django)
    (should (tern-django-running-p))))

(ert-deftest test-tern-django-run-single-process-at-time ()
  "Check we run only one `tern-django' script instance."
  (let ((tern-django-process (start-process "cat" nil "cat")))
    (tern-django)
    (should (equal "cat" (car (process-command tern-django-process))))))

(provide 'tern-django-test)

;;; tern-django-test.el ends here
