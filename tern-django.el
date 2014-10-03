;;; tern-django.el --- Create tern projects for django applications.

;; Copyright (C) 2014 by Malyshev Artem

;; Author: Malyshev Artem <proofit404@gmail.com>
;; URL: https://github.com/proofit404/tern-django
;; Version: 0.0.1
;; Package-Requires: ((emacs "24") (tern "0.0.1"))

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program. If not, see <http://www.gnu.org/licenses/>.

;;; Installation:

;; You can install this package from Melpa:
;;
;;     M-x package-install RET relative-buffers RET

;;; Commentary:

;; Obviously all JavaScript code of application stored in application
;; static folder.  So we can write standard .tern-project file into
;; each application root.  We can add custom JavaScript from templates
;; script tags.  So we can extend default "libs", "loadEagerly" and
;; "plugins" settings.  Also if template use external library from
;; internet we can download it to temporary folder and make it
;; accessible for tern.
;;
;; `django-tern' command do following:
;;
;; * Check if DJANGO_SETTINGS_MODULE was specified
;; * Call python script
;; * For each application parse each file in templates directory
;; * Look in script tags for specified static files
;; * Save parse result with file modification date in sqlite3 database
;; * Write .tern-project file if necessary

;;; Usage:

;; Drop following line into your .emacs file:
;;
;;     (add-hook 'after-save-hook 'tern-django)
;;
;; Setup your project variables:
;;
;;     M-x setenv RET DJANGO_SETTINGS_MODULE RET project.settings
;;     M-x setenv RET PYTHONPATH RET /home/user/path/to/project/
;;
;; When you save any file all tern-project settings will be updated to
;; the most resent changes.

;;; Code:

(provide 'tern-django)

;;; tern-django.el ends here
