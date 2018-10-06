IMAGE_NAME ?= codeclimate/codeclimate-bandit

.PHONY: release

release:
	docker build --tag $(IMAGE_NAME) .
