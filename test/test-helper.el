;;; test-helper.el --- ert-runner test helper

;;; Commentary:

;;; Code:

(require 'cask)

(let ((root-directory (locate-dominating-file load-file-name "Cask")))
  (cask-initialize root-directory)
  (add-to-list 'load-path root-directory))

(defun wait-for-tern-django ()
  "Helper function waiting for `tern-django' process to finish."
  (while (tern-django-running-p)
    (accept-process-output tern-django-process))
  (funcall (process-sentinel tern-django-process)
           tern-django-process
           "finished\n"))

(provide 'test-helper)

;;; test-helper.el ends here
