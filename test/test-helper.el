;;; test-helper.el --- ert-runner test helper

;;; Commentary:

;;; Code:

(require 'cask)

(require 'undercover)
(undercover "tern-django.el" (:report-file "emacs-coveralls.json"))

(let ((root-directory (locate-dominating-file load-file-name "Cask")))
  (cask-initialize root-directory)
  (add-to-list 'load-path root-directory))

(provide 'test-helper)

;;; test-helper.el ends here
