;;; warlock-mode.el --- Description -*- lexical-binding: t; -*-
;;
;; Copyright (C) 2021 Laurence Pakenham-Smith
;;
;; Author: Laurence Pakenham-Smith <https://github.com/laurence>
;; Maintainer: Laurence Pakenham-Smith <laurence@sourceless.org>
;; Created: March 13, 2021
;; Modified: March 13, 2021
;; Version: 0.0.1
;; Keywords: Symbol’s value as variable is void: finder-known-keywords
;; Homepage: https://github.com/laurence/warlock-mode
;; Package-Requires: ((emacs "24.3"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;;  Description
;;
;;; Code:
(setq warlock-highlights
      '(("#.*$" . font-lock-comment-face )
        ("fn\\|let\\|define\\|macro\\|type\\|def" . font-lock-keyword-face)
        ("\\".+\\"" . font-lock-string-face)
        ))

(define-derived-mode warlock-mode fundamental-mode "warlock"
  "Major mode for editing Warlock code."
  (setq font-lock-defaults '(warlock-highlights)))


(provide 'warlock-mode)
;;; warlock-mode.el ends here
