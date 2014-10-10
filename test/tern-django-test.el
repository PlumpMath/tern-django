;;; tern-django-test.el --- tern-django test suite

;;; Commentary:

;;; Code:

(require 'ert)
(require 'tern-django)

(ert-deftest test-tern-django-run-command ()
  (let ((tenr-django-script "-V"))
    (tern-django)
    (should (processp tern-django-process))))

(provide 'tern-django-test)

;;; tern-django-test.el ends here